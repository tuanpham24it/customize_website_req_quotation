from odoo import http
from odoo.http import request

class WebsiteRequestQuote(http.Controller):

    @http.route(
        '/shop/request_quote',
        type='http',
        auth='public',
        website=True,
        csrf=True
    )
    def request_quote(self, **post):

        cart = request.website.sale_get_order()
        if not cart or not cart.order_line:
            return request.redirect('/shop/cart')

        # 1. Tìm contact khách hàng hoặc tạo mới
        Partner = request.env['res.partner'].sudo()
        partner = Partner.search([
            '|',
            ('email', '=', post.get('email')),
            ('phone', '=', post.get('phone')),
        ], limit=1)

        if not partner:
            partner = Partner.create({
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'customer_rank': 1,
            })

        # 2. Tạo báo giá (quatotion) mới
        SaleOrder = request.env['sale.order'].sudo()
        quotation = SaleOrder.create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'website_id': request.website.id,
            'origin': f"Website Request Quote #{cart.name}",
        })

        # 3. Lấy các sản phẩm từ Cart và thêm vào báo giá
        for line in cart.order_line:
            request.env['sale.order.line'].sudo().create({
                'order_id': quotation.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'name': line.name,
            })

        # 4. LOG
        quotation.message_post(
            body="Khách hàng gửi yêu cầu báo giá từ giỏ hàng website."
        )

        # 5. Reset giỏ hàng (Xóa các sản phẩm trong giỏ hàng)
        # request.website.sale_reset()

        return request.redirect('/thank-you')
