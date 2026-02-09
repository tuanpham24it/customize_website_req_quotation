{
    "name": "Customize Website Request Quotation",
    "version": "18.1.0",
    "summary": "Request quotation from cart",
    "category": "Website",
    "depends": [
        "website",
        "website_sale",
        "sale",
    ],
    "data": [
        "views/cart_custom.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "customize_module/static/src/js/request_quote.js",
        ],
    },

    "installable": True,
    "license": "LGPL-3",
}
