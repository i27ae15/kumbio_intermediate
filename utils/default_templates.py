DEFAULT_TEMPLATES = [

    {
        'name': 'Confirmación',
        'subject': 'Confirmación de tu cita Día: {date} - Hora: {time}',
        'message': """
            <head>
            <title></title>
            <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
            <meta content="width=device-width, initial-scale=1.0" name="viewport" />
            <!--[if mso
            ]><xml
                ><o:OfficeDocumentSettings
                ><o:PixelsPerInch>96</o:PixelsPerInch
                ><o:AllowPNG /></o:OfficeDocumentSettings></xml
            ><![endif]-->
            <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
            }

            a[x-apple-data-detectors] {
                color: inherit !important;
                text-decoration: inherit !important;
            }

            #MessageViewBody a {
                color: inherit;
                text-decoration: none;
            }

            p {
                line-height: inherit;
            }

            .desktop_hide,
            .desktop_hide table {
                mso-hide: all;
                display: none;
                max-height: 0px;
                overflow: hidden;
            }

            @media (max-width: 660px) {
                .desktop_hide table.icons-inner {
                display: inline-block !important;
                }

                .icons-inner {
                text-align: center;
                }

                .icons-inner td {
                margin: 0 auto;
                }

                .image_block img.big,
                .row-content {
                width: 100% !important;
                }

                .mobile_hide {
                display: none;
                }

                .stack .column {
                width: 100%;
                display: block;
                }

                .mobile_hide {
                min-height: 0;
                max-height: 0;
                max-width: 0;
                overflow: hidden;
                font-size: 0px;
                }

                .desktop_hide,
                .desktop_hide table {
                display: table !important;
                max-height: none !important;
                }
            }
            </style>
        </head>
        <body
            style="
            background-color: #f3f2f3;
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: none;
            text-size-adjust: none;
            "
        >
            <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            class="nl-container"
            role="presentation"
            style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                background-color: #f3f2f3;
            "
            width="100%"
            >
            <tbody>
                <tr>
                <td>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-1"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-1 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 30px solid #f3f2f3;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-2"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 33px;
                                        "
                                        >
                                        <div
                                            align="left"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="I'm an image"
                                            src="https://i.ibb.co/dmG2tgn/logo-pixelado-T-sin-pajaro.png" alt="logo-pixelado-T-sin-pajaro"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 80px;
                                                max-width: 100%;
                                            "
                                            title="I'm an image"
                                            width="154"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="empty_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div></div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-3"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 5px;
                                        line-height: 5px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            padding-top: 30px;
                                        "
                                        >
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-bottom: 33px">
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 21.6px;
                                                color: #555555;
                                                line-height: 1.8;
                                            "
                                            >
                                            <h3
                                                style="
                                                margin: 0 25px 0 -50px;
                                                font-size: 16px;
                                                text-align: center;
                                                mso-line-height-alt: 19.2px;
                                                "
                                            >
                                                <span style="color: #004afd"
                                                ><strong>{organization_name}</strong></span
                                                >
                                            </h3>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-3"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-4"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                background-image: url('images/bg-reminder.jpg');
                                background-position: center top;
                                background-repeat: repeat;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 60px;
                                        line-height: 60px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 30px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 10px;
                                            padding-left: 48px;
                                            padding-right: 48px;
                                            padding-top: 10px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 14px;
                                                mso-line-height-alt: 16.8px;
                                                color: #555555;
                                                line-height: 1.2;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 42px;
                                                    color: #2a272b;
                                                "
                                                ><strong
                                                    >Usted tiene una cita con
                                                    {calendar_user}</strong
                                                ></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-4 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 20px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-5"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            class="big"
                                            src="https://i.ibb.co/crF0zpv/reminder-hero-graph.png" alt="reminder-hero-graph"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 640px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="640"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-5"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-6"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 24px;
                                    padding-right: 24px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="50%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 60px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            src="https://i.ibb.co/HrNt4ZS/Time.png"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 96px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="96"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 10px;
                                            padding-top: 18px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 14px;
                                                mso-line-height-alt: 16.8px;
                                                color: #555555;
                                                line-height: 1.2;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 20px;
                                                    color: #2a272b;
                                                "
                                                ><strong>{date}, {time}</strong></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 24px;
                                    padding-right: 24px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="50%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 40px;
                                        line-height: 40px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 20px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            src="https://i.ibb.co/x84nvKs/Location.png"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 96px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="96"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-4"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 65px;
                                            padding-top: 18px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 14px;
                                                mso-line-height-alt: 16.8px;
                                                color: #555555;
                                                line-height: 1.2;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 20px;
                                                    color: #2a272b;
                                                "
                                                ><strong>{place}</strong></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-7"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="10"
                                    cellspacing="0"
                                    class="paragraph_block block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div
                                            style="
                                            color: #070707;
                                            font-size: 14px;
                                            font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            font-weight: 400;
                                            line-height: 180%;
                                            text-align: center;
                                            direction: ltr;
                                            letter-spacing: 0px;
                                            mso-line-height-alt: 25.2px;
                                            "
                                        >
                                            <div style="margin: 0 100px">
                                            <p style="margin: 10px">
                                                Sr.(a): {attendee_name}. Recibe un
                                                cordial saludo, confirmamos tu cita
                                            </p>
                                            <p>
                                                Si por alguna razón no puedes asistir a
                                                tu cita, por favor ingresa con tu código
                                                de cita y modifícala hasta con 12 horas
                                                de anticipación.
                                            </p>
                                            <p>Tu código de cita es: {code}</p>
                                            <br />Te esperamos. <br />Muchas gracias
                                            por utilizar nuestros servicios.
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-8"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    padding-right: 24px;
                                    vertical-align: top;
                                    padding-top: 56px;
                                    padding-bottom: 48px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-9"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-10"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 33px;
                                        "
                                        >
                                        <div
                                            align="left"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="I'm an image"
                                            src="https://i.ibb.co/dmG2tgn/logo-pixelado-T-sin-pajaro.png" alt="logo-pixelado-T-sin-pajaro"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 80px;
                                                max-width: 100%;
                                                margin-bottom: 15%;
                                            "
                                            title="I'm an image"
                                            width="154"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="empty_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div></div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-3"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 5px;
                                        line-height: 5px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            padding-top: 30px;
                                        "
                                        >
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 33px;
                                            padding-right: 48px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 18px;
                                                color: #555555;
                                                line-height: 1.5;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: left;
                                                mso-line-height-alt: 21px;
                                                "
                                            >
                                                Copyright © 2022
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-11"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="15"
                                    cellspacing="0"
                                    class="divider_block mobile_hide block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-12"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 5px;
                                    padding-bottom: 5px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="icons_block block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            vertical-align: middle;
                                            color: #9d9d9d;
                                            font-family: inherit;
                                            font-size: 15px;
                                            padding-bottom: 5px;
                                            padding-top: 5px;
                                            text-align: center;
                                        "
                                        >
                                        <table
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                            mso-table-lspace: 0pt;
                                            mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                        >
                                            <tr>
                                            <td
                                                class="alignment"
                                                style="
                                                vertical-align: middle;
                                                text-align: center;
                                                "
                                            >
                                                <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                                <!--[if !vml]><!-->
                                                <table
                                                cellpadding="0"
                                                cellspacing="0"
                                                class="icons-inner"
                                                role="presentation"
                                                style="
                                                    mso-table-lspace: 0pt;
                                                    mso-table-rspace: 0pt;
                                                    display: inline-block;
                                                    margin-right: -4px;
                                                    padding-left: 0px;
                                                    padding-right: 0px;
                                                "
                                                ></table>
                                            </td>
                                            </tr>
                                        </table>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                </td>
                </tr>
            </tbody>
            </table>
 
        """,
        'template_type': 0,
    },

    {
        'name': 'Recordatorio',
        'subject': 'Recordatorio de tu cita Día: {date} - Hora: {time}',
        'message': """
          <head>
            <title></title>
            <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
            <meta content="width=device-width, initial-scale=1.0" name="viewport" />
            <!--[if mso
            ]><xml
                ><o:OfficeDocumentSettings
                ><o:PixelsPerInch>96</o:PixelsPerInch
                ><o:AllowPNG /></o:OfficeDocumentSettings></xml
            ><![endif]-->
            <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
            }

            a[x-apple-data-detectors] {
                color: inherit !important;
                text-decoration: inherit !important;
            }

            #MessageViewBody a {
                color: inherit;
                text-decoration: none;
            }

            p {
                line-height: inherit;
            }

            .desktop_hide,
            .desktop_hide table {
                mso-hide: all;
                display: none;
                max-height: 0px;
                overflow: hidden;
            }

            @media (max-width: 660px) {
                .desktop_hide table.icons-inner {
                display: inline-block !important;
                }

                .icons-inner {
                text-align: center;
                }

                .icons-inner td {
                margin: 0 auto;
                }

                .image_block img.big,
                .row-content {
                width: 100% !important;
                }

                .mobile_hide {
                display: none;
                }

                .stack .column {
                width: 100%;
                display: block;
                }

                .mobile_hide {
                min-height: 0;
                max-height: 0;
                max-width: 0;
                overflow: hidden;
                font-size: 0px;
                }

                .desktop_hide,
                .desktop_hide table {
                display: table !important;
                max-height: none !important;
                }
            }
            </style>
        </head>
        <body
            style="
            background-color: #f3f2f3;
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: none;
            text-size-adjust: none;
            "
        >
            <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            class="nl-container"
            role="presentation"
            style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                background-color: #f3f2f3;
            "
            width="100%"
            >
            <tbody>
                <tr>
                <td>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-1"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-1 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 30px solid #f3f2f3;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-2"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 33px;
                                        "
                                        >
                                        <div
                                            align="left"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="I'm an image"
                                            src="https://i.ibb.co/dmG2tgn/logo-pixelado-T-sin-pajaro.png" alt="logo-pixelado-T-sin-pajaro"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 80px;
                                                max-width: 100%;
                                            "
                                            title="I'm an image"
                                            width="154"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="empty_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div></div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-3"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 5px;
                                        line-height: 5px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            padding-top: 30px;
                                        "
                                        >
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-bottom: 33px">
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 21.6px;
                                                color: #555555;
                                                line-height: 1.8;
                                            "
                                            >
                                            <h3
                                                style="
                                                margin: 0 25px 0 -50px;
                                                font-size: 16px;
                                                text-align: center;
                                                mso-line-height-alt: 19.2px;
                                                "
                                            >
                                                <span style="color: #004afd"
                                                ><strong>{organization_name}</strong></span
                                                >
                                            </h3>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-3"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-4"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                background-image: url('images/bg-reminder.jpg');
                                background-position: center top;
                                background-repeat: repeat;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 60px;
                                        line-height: 60px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 30px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 10px;
                                            padding-left: 48px;
                                            padding-right: 48px;
                                            padding-top: 10px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 14px;
                                                mso-line-height-alt: 16.8px;
                                                color: #555555;
                                                line-height: 1.2;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 42px;
                                                    color: #2a272b;
                                                "
                                                ><strong
                                                    >Recordatorio de tu cita con {organizaction_name}</strong
                                                ></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-4 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 20px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-5"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            class="big"
                                            src="https://i.ibb.co/crF0zpv/reminder-hero-graph.png" alt="reminder-hero-graph"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 640px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="640"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-5"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-6"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 24px;
                                    padding-right: 24px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="50%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 60px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            src="https://i.ibb.co/HrNt4ZS/Time.png"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 96px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="96"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 10px;
                                            padding-top: 18px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 14px;
                                                mso-line-height-alt: 16.8px;
                                                color: #555555;
                                                line-height: 1.2;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 20px;
                                                    color: #2a272b;
                                                "
                                                ><strong>{date}, {time}</strong></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 24px;
                                    padding-right: 24px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="50%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 40px;
                                        line-height: 40px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 20px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            src="https://i.ibb.co/x84nvKs/Location.png"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 96px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="96"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-4"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 65px;
                                            padding-top: 18px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 14px;
                                                mso-line-height-alt: 16.8px;
                                                color: #555555;
                                                line-height: 1.2;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 20px;
                                                    color: #2a272b;
                                                "
                                                ><strong>{place}</strong></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-7"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="10"
                                    cellspacing="0"
                                    class="paragraph_block block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div
                                            style="
                                            color: #070707;
                                            font-size: 14px;
                                            font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            font-weight: 400;
                                            line-height: 180%;
                                            text-align: center;
                                            direction: ltr;
                                            letter-spacing: 0px;
                                            mso-line-height-alt: 25.2px;
                                            "
                                        >
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-8"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >

                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-9"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-10"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 33px;
                                        "
                                        >
                                        <div
                                            align="left"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="I'm an image"
                                            src="https://i.ibb.co/dmG2tgn/logo-pixelado-T-sin-pajaro.png" alt="logo-pixelado-T-sin-pajaro"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 80px;
                                                max-width: 100%;
                                                margin-bottom: 15%;
                                            "
                                            title="I'm an image"
                                            width="154"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="empty_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div></div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-3"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 5px;
                                        line-height: 5px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            padding-top: 30px;
                                        "
                                        >
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 33px;
                                            padding-right: 48px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 18px;
                                                color: #555555;
                                                line-height: 1.5;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: left;
                                                mso-line-height-alt: 21px;
                                                "
                                            >
                                                Copyright © 2022
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-11"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="15"
                                    cellspacing="0"
                                    class="divider_block mobile_hide block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-12"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 5px;
                                    padding-bottom: 5px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="icons_block block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            vertical-align: middle;
                                            color: #9d9d9d;
                                            font-family: inherit;
                                            font-size: 15px;
                                            padding-bottom: 5px;
                                            padding-top: 5px;
                                            text-align: center;
                                        "
                                        >
                                        <table
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                            mso-table-lspace: 0pt;
                                            mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                        >
                                            <tr>
                                            <td
                                                class="alignment"
                                                style="
                                                vertical-align: middle;
                                                text-align: center;
                                                "
                                            >
                                                <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                                <!--[if !vml]><!-->
                                                <table
                                                cellpadding="0"
                                                cellspacing="0"
                                                class="icons-inner"
                                                role="presentation"
                                                style="
                                                    mso-table-lspace: 0pt;
                                                    mso-table-rspace: 0pt;
                                                    display: inline-block;
                                                    margin-right: -4px;
                                                    padding-left: 0px;
                                                    padding-right: 0px;
                                                "
                                                ></table>
                                            </td>
                                            </tr>
                                        </table>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                </td>
                </tr>
            </tbody>
            </table>
            <!-- End -->
        </body>
        
        """,
        'template_type': 1,
    },

    {
        'name': 'Reagendado',
        'subject': 'Re-programación de tu cita Día: {date} - Hora: {time}',
        'message': '<p>Te confirmamos que tu cita ha sido reagendada para:</p> <p>Día: {date}.</p> <p>Hora: {time}. <p>Fecha anterior:</p> <p>Día: {old_day}.</p> <p>Hora: {old_time} </p>  <p>Su codigo de cita es: {code}</p> <p> Muchas gracias por preferirnos.</p> <p>Lo esperamos</p>',
        'template_type': 4,
    },

    {
        'name': 'Cancelación',
        'subject': 'Cancelación de su cita para el día: {date} a las: {time}.',
        'message': """
        <head>
            <title></title>
            <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
            <meta content="width=device-width, initial-scale=1.0" name="viewport" />
            <!--[if mso
            ]><xml
                ><o:OfficeDocumentSettings
                ><o:PixelsPerInch>96</o:PixelsPerInch
                ><o:AllowPNG /></o:OfficeDocumentSettings></xml
            ><![endif]-->
            <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
            }

            a[x-apple-data-detectors] {
                color: inherit !important;
                text-decoration: inherit !important;
            }

            #MessageViewBody a {
                color: inherit;
                text-decoration: none;
            }

            p {
                line-height: inherit;
            }

            .desktop_hide,
            .desktop_hide table {
                mso-hide: all;
                display: none;
                max-height: 0px;
                overflow: hidden;
            }

            @media (max-width: 660px) {
                .desktop_hide table.icons-inner {
                display: inline-block !important;
                }

                .icons-inner {
                text-align: center;
                }

                .icons-inner td {
                margin: 0 auto;
                }

                .image_block img.big,
                .row-content {
                width: 100% !important;
                }

                .mobile_hide {
                display: none;
                }

                .stack .column {
                width: 100%;
                display: block;
                }

                .mobile_hide {
                min-height: 0;
                max-height: 0;
                max-width: 0;
                overflow: hidden;
                font-size: 0px;
                }

                .desktop_hide,
                .desktop_hide table {
                display: table !important;
                max-height: none !important;
                }
            }
            </style>
        </head>
        <body
            style="
            background-color: #f3f2f3;
            margin: 0;
            padding: 0;
            -webkit-text-size-adjust: none;
            text-size-adjust: none;
            "
        >
            <table
            border="0"
            cellpadding="0"
            cellspacing="0"
            class="nl-container"
            role="presentation"
            style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                background-color: #f3f2f3;
            "
            width="100%"
            >
            <tbody>
                <tr>
                <td>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-1"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-1 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 30px solid #f3f2f3;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-2"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 33px;
                                        "
                                        >
                                        <div
                                            align="left"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="I'm an image"
                                            src="https://i.ibb.co/dmG2tgn/logo-pixelado-T-sin-pajaro.png"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 80px;
                                                max-width: 100%;
                                            "
                                            title="I'm an image"
                                            width="154"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="empty_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div></div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-3"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 5px;
                                        line-height: 5px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            padding-top: 30px;
                                        "
                                        >
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-bottom: 33px">
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 21.6px;
                                                color: #555555;
                                                line-height: 1.8;
                                            "
                                            >
                                            <h3
                                                style="
                                                margin: 0 25px 0 -50px;
                                                font-size: 16px;
                                                text-align: center;
                                                mso-line-height-alt: 19.2px;
                                                "
                                            >
                                                <span style="color: #004afd"
                                                ><strong
                                                    >{organization_name}</strong
                                                ></span
                                                >
                                            </h3>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-3"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-4"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                background-image: url('images/bg-shade.jpg');
                                background-position: center top;
                                background-repeat: repeat;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr style="background: white">
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad" style="padding-top: 50px">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 14.399999999999999px;
                                                color: #555555;
                                                line-height: 1.2;
                                            "
                                            ></div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-4"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 15px;
                                            padding-left: 38px;
                                            padding-right: 38px;
                                            padding-top: 20px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 14.399999999999999px;
                                                color: #555555;
                                                line-height: 1.2;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: center;
                                                mso-line-height-alt: 16.8px;
                                                "
                                            >
                                                <span
                                                style="
                                                    font-size: 42px;
                                                    color: #2a272b;
                                                "
                                                ><strong
                                                    >Su cita ha sido cancelada</strong
                                                ></span
                                                >
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-5"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 10px;
                                            padding-left: 38px;
                                            padding-right: 38px;
                                            padding-top: 10px;
                                        "
                                        >
                                        <div style="font-family: Arial, sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Arial, 'Helvetica Neue',
                                                Helvetica, sans-serif;
                                                mso-line-height-alt: 18px;
                                                color: #555555;
                                                line-height: 1.5;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                text-align: center;
                                                mso-line-height-alt: 24px;
                                                "
                                            >
                                                <span style="font-size: 16px"
                                                >Su cita para el día: {date} a las:
                                                {time} ha sido cancelada.
                                                <br />
                                                Si desea reagendar su cita por favor
                                                ingrese de nuevo a nuestro portal con
                                                el codigo {code}.
                                                <br />
                                                </span>
                                            </p>
                                            <p
                                                style="
                                                margin: 0;
                                                mso-line-height-alt: 18px;
                                                "
                                            >
                                                 
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="heading_block block-6"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="width: 100%; text-align: center"
                                        >
                                        <h1
                                            style="
                                            margin: 0;
                                            color: #555555;
                                            font-size: 23px;
                                            font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                            line-height: 120%;
                                            text-align: center;
                                            direction: ltr;
                                            font-weight: 700;
                                            letter-spacing: normal;
                                            margin-top: 0;
                                            margin-bottom: 0;
                                            "
                                        >
                                            <span class="tinyMce-placeholder"
                                            >¡Gracias por elegirnos!</span
                                            >
                                        </h1>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-7"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                        "
                                        >
                                        <div
                                            align="center"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="Image"
                                            class="big"
                                            src="https://i.ibb.co/crF0zpv/reminder-hero-graph.png" alt="reminder-hero-graph"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 640px;
                                                max-width: 100%;
                                            "
                                            title="Image"
                                            width="640"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-5"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 1px;
                                        line-height: 1px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-6"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #ffffff;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="image_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            width: 100%;
                                            padding-right: 0px;
                                            padding-left: 0px;
                                            padding-top: 33px;
                                        "
                                        >
                                        <div
                                            align="left"
                                            class="alignment"
                                            style="line-height: 10px"
                                        >
                                            <img
                                            alt="I'm an image"
                                            src="https://i.ibb.co/dmG2tgn/logo-pixelado-T-sin-pajaro.png"
                                            style="
                                                display: block;
                                                height: auto;
                                                border: 0;
                                                width: 80px;
                                                max-width: 100%;
                                            "
                                            title="I'm an image"
                                            width="154"
                                            />
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-2"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="empty_block block-2"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div></div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                <td
                                    class="column column-3"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    padding-left: 48px;
                                    vertical-align: top;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="33.333333333333336%"
                                >
                                    <div
                                    class="spacer_block"
                                    style="
                                        height: 5px;
                                        line-height: 5px;
                                        font-size: 1px;
                                    "
                                    >
                                     
                                    </div>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="divider_block block-2 mobile_hide"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            padding-top: 30px;
                                        "
                                        >
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="text_block block-3"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        word-break: break-word;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            padding-bottom: 33px;
                                            padding-right: 48px;
                                        "
                                        >
                                        <div style="font-family: sans-serif">
                                            <div
                                            class=""
                                            style="
                                                font-size: 12px;
                                                font-family: Helvetica Neue, Helvetica,
                                                Arial, sans-serif;
                                                mso-line-height-alt: 18px;
                                                color: #555555;
                                                line-height: 1.5;
                                            "
                                            >
                                            <p
                                                style="
                                                margin: 0;
                                                font-size: 14px;
                                                text-align: left;
                                                mso-line-height-alt: 21px;
                                                "
                                            >
                                                {doctor_name}
                                            </p>
                                            </div>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-7"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                background-color: #f3f2f3;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 0px;
                                    padding-bottom: 0px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="15"
                                    cellspacing="0"
                                    class="divider_block mobile_hide block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td class="pad">
                                        <div align="center" class="alignment">
                                            <table
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                            >
                                            <tr>
                                                <td
                                                class="divider_inner"
                                                style="
                                                    font-size: 1px;
                                                    line-height: 1px;
                                                    border-top: 0px solid #bbbbbb;
                                                "
                                                >
                                                <span> </span>
                                                </td>
                                            </tr>
                                            </table>
                                        </div>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                    <table
                    align="center"
                    border="0"
                    cellpadding="0"
                    cellspacing="0"
                    class="row row-8"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt"
                    width="100%"
                    >
                    <tbody>
                        <tr>
                        <td>
                            <table
                            align="center"
                            border="0"
                            cellpadding="0"
                            cellspacing="0"
                            class="row-content stack"
                            role="presentation"
                            style="
                                mso-table-lspace: 0pt;
                                mso-table-rspace: 0pt;
                                color: #000000;
                                width: 640px;
                            "
                            width="640"
                            >
                            <tbody>
                                <tr>
                                <td
                                    class="column column-1"
                                    style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    font-weight: 400;
                                    text-align: left;
                                    vertical-align: top;
                                    padding-top: 5px;
                                    padding-bottom: 5px;
                                    border-top: 0px;
                                    border-right: 0px;
                                    border-bottom: 0px;
                                    border-left: 0px;
                                    "
                                    width="100%"
                                >
                                    <table
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    class="icons_block block-1"
                                    role="presentation"
                                    style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                    "
                                    width="100%"
                                    >
                                    <tr>
                                        <td
                                        class="pad"
                                        style="
                                            vertical-align: middle;
                                            color: #9d9d9d;
                                            font-family: inherit;
                                            font-size: 15px;
                                            padding-bottom: 5px;
                                            padding-top: 5px;
                                            text-align: center;
                                        "
                                        >
                                        <table
                                            cellpadding="0"
                                            cellspacing="0"
                                            role="presentation"
                                            style="
                                            mso-table-lspace: 0pt;
                                            mso-table-rspace: 0pt;
                                            "
                                            width="100%"
                                        >
                                            <tr>
                                            <td
                                                class="alignment"
                                                style="
                                                vertical-align: middle;
                                                text-align: center;
                                                "
                                            >
                                                <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                                <!--[if !vml]><!-->
                                                <table
                                                cellpadding="0"
                                                cellspacing="0"
                                                class="icons-inner"
                                                role="presentation"
                                                style="
                                                    mso-table-lspace: 0pt;
                                                    mso-table-rspace: 0pt;
                                                    display: inline-block;
                                                    margin-right: -4px;
                                                    padding-left: 0px;
                                                    padding-right: 0px;
                                                "
                                                >
                                                <!--<![endif]-->
                                                </table>
                                            </td>
                                            </tr>
                                        </table>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                                </tr>
                            </tbody>
                            </table>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                </td>
                </tr>
            </tbody>
            </table>
            <!-- End -->
        </body>

""",
        'template_type': 5,
    },

    {
        'name': 'Nuevo cliente (organization)',
        'subject': 'Nuevo Cliente ',
        'message': '<p>Una nueva cita ha sido agendada</p> <p>Nombre de la persona: {attendee_name}</p> <p>Fecha: {date}</p> <p>Hora {time}</p>',
        'template_type': 6,
    },

    {
        'name': 'Reagendado (organization)',
        'subject': 'Cita re-agendada (organization)',
        'message': '<p>La cita con la fecha {old_day}, y la hora {old_time}, ha sido reagendada</p><p>Nueva fecha: {date}</p> <p>nueva hora {time}</p>',
        'template_type': 7,
    },
    
    {
        'name': 'Cancelación (organization)',
        'subject': 'Cita cancelada (organization)',
        'message': '<p>la cita con la fecha {date}, y la hora {time}, ha sido cancelada</p>',
        'template_type': 8,
    }
]


