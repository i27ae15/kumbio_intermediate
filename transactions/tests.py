from django.urls import reverse

from rest_framework.test import APITestCase

from organization_info.tests import (create_user, create_organization, set_authorization, create_client,
create_place, create_service, create_professional, create_client_type)

from organization_info.models.main_models import PaymentMethodAcceptedByOrg, Organization

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

class TestAppointmentInvoice(APITestCase):

    def setUp(self) -> None:
        self.organization = create_organization()
        self.user = create_user(organization=self.organization)
        self.clients = create_client(organization=self.organization, client_type=create_client_type(self.organization))
        self.professional = create_professional(organization=self.organization)
        self.organization_place = create_place(data_to_create_place={}, user=self.user, organization=self.organization, create_with_serializer=False)
        self.service = create_service(data_to_create_service={}, organization=self.organization, create_with_serializer=False)

        self.payment_methods = create_default_payment_methods(self.organization)
        set_authorization(self.client)

        return super().setUp()
    

    def test_create_invoice(self):

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










