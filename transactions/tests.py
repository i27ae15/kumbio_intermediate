import random

from django.urls import reverse

from rest_framework.test import APITestCase

from organization_info.tests import (create_user, create_organization, set_authorization, create_client,
create_place, create_service, create_professional, create_client_type)

from organization_info.models.main_models import PaymentMethodAcceptedByOrg, Organization
from .models import AppointmentInvoice
from .serializers import AppointmentInvoiceSerializer

from print_pp.logging import Print


def create_default_payment_methods(add_to_organization:Organization=None) -> list[PaymentMethodAcceptedByOrg]:
    payment_methods = [
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Efectivo"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Tarjeta de crédito"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Tarjeta de débito"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Transferencia bancaria"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Cheque"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="PayPal"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Bitcoin"
        ),
        PaymentMethodAcceptedByOrg.objects.create(
            payment_method="Otro"
        )
    ]

    if add_to_organization:
        for method in payment_methods:
            add_to_organization.payment_methods_accepted.add(method)

    return payment_methods


def create_invoices(user=None, organization=None, clients=None, professional=None, organization_place=None, service=None, num_invoices=10) -> tuple[list[AppointmentInvoice], tuple]:

    """
        This will create a N number of invoices and return them in a list plus the user, organization, professional, organization_place 
        and service used to create them, in that order
    """

    organization = create_organization() if not organization else organization
    user = create_user(organization=organization) if not user else user
    clients = create_client(organization=organization, client_type=create_client_type(organization), num_clients=num_invoices) if not clients else clients
    professional = create_professional(organization=organization) if not professional else professional
    organization_place = create_place(data_to_create_place={}, user=user, organization=organization, create_with_serializer=False) if not organization_place else organization_place
    service = create_service(data_to_create_service={}, organization=organization, create_with_serializer=False) if not service else service

    payment_methods = create_default_payment_methods(organization)
    invoices = []
    tax = 0.16

    items_used_to_create_invoices = (user, organization, professional, organization_place, service)

    for i in range(1, num_invoices + 1):
        amount = float(random.randint(50, 120))
        decimal_part = random.randint(0, 20)

        discount = float(f'0.{decimal_part}')
        total = round(float(amount + (amount * tax) - (amount * discount)), 2)

        data_to_create_invoice_successfully = {
            'appointment_id': i,
            'organization': organization.pk,
            'payment_method': payment_methods[0].pk,
            'client': clients[i - 1].pk,
            'professional': professional.pk,
            'place': organization_place.pk,
            'services': [service.pk],
            'amount': amount,
            'tax': tax,
            'discount': discount,
            'total': total,
            'total_paid': total,
            'payment_date': '2022-12-02',
            'payment_reference': '1234567890',
            'payment_notes': 'Pago realizado con tarjeta de crédito',
            'created_by': user.pk
        }

        serializer = AppointmentInvoiceSerializer(data=data_to_create_invoice_successfully)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        invoices.append(serializer.instance)


    return invoices, items_used_to_create_invoices

class TestAppointmentInvoice(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(organization=self.organization)
        self.clients = create_client(organization=self.organization, client_type=create_client_type(self.organization), num_clients=10)
        self.professional = create_professional(organization=self.organization)
        self.organization_place = create_place(data_to_create_place={}, user=self.user, organization=self.organization, create_with_serializer=False)
        self.service = create_service(data_to_create_service={}, organization=self.organization, create_with_serializer=False)

        self.payment_methods = create_default_payment_methods(self.organization)
        set_authorization(self.client)

        return super().setUp()
    

    def test_create_invoice_through_api(self):

        url = reverse('transactions:appointment_invoice')

        amount = 115.00
        tax = 0.16
        discount = 0.00

        total = float(amount + (amount * tax) - (amount * discount))

        data_to_create_invoice_successfully = {
            'appointment_id': 115,
            'organization': self.organization.pk,
            'payment_method': self.payment_methods[0].pk,
            'client': self.clients[0].pk,
            'professional': self.professional.pk,
            'place': self.organization_place.pk,
            'services': [self.service.pk],
            'amount': amount,
            'tax': tax,
            'discount': 0.00,
            'total': total,
            'total_paid': total,
            'payment_date': '2022-12-02',
            'payment_reference': '1234567890',
            'payment_notes': 'Pago realizado con tarjeta de crédito',
        }

        response = self.client.post(url, data_to_create_invoice_successfully, format='json')
        
        if response.status_code != 201:
            Print('json', response.json())
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 1)

        
        data_to_create_invoice_unsuccessfully = {
            'appointment_id': 115,
            'organization': self.organization.pk,
            'payment_method': self.payment_methods[0].pk,
            'client': self.clients[0].pk,
            'professional': self.professional.pk,
            'place': self.organization_place.pk,
            'services': [self.service.pk],
            'amount': amount,
            'tax': tax,
            'discount': 0.00,
            'total': total + 10,
            'total_paid': total,
            'payment_date': '2022-12-02',
            'payment_reference': '1234567890',
            'payment_notes': 'Pago realizado con tarjeta de crédito',
        }

        response = self.client.post(url, data_to_create_invoice_unsuccessfully, format='json')
        self.assertEqual(response.status_code, 400)


        data_to_create_invoice_pending = {
            'appointment_id': 115,
            'organization': self.organization.pk,
            'payment_method': self.payment_methods[0].pk,
            'client': self.clients[0].pk,
            'professional': self.professional.pk,
            'place': self.organization_place.pk,
            'services': [self.service.pk],
            'amount': amount,
            'tax': tax,
            'discount': 0.00,
            'total': total,
            'total_paid': total - 10,
            'payment_date': '2022-12-02',
            'payment_reference': '1234567890',
            'payment_notes': 'Pago realizado con tarjeta de crédito',
        }

        response = self.client.post(url, data_to_create_invoice_pending, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 2)


    def test_get_invoices_through_api(self):
        invoices, items_used_to_create_invoices = create_invoices(
            self.user, 
            self.organization, 
            self.clients, 
            self.professional, 
            self.organization_place, 
            self.service,
            num_invoices=len(self.clients)
        )

        url = reverse('transactions:appointment_invoice')

        response = self.client.get(url, {'from_date':'2021-12-12'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)

        url = reverse('transactions:appointment_invoice')

        # response = self.client.get(url, {'invoice_id': invoices[0].pk}, format='json')
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['id'], invoices[0].pk)






