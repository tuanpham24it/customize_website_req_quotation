odoo.define('customize_module.request_quote', [], function () {
    'use strict';

    function showModal(modal) {
        modal.classList.add('show');
        modal.style.display = 'block';
        modal.removeAttribute('aria-hidden');
        document.body.classList.add('modal-open');

        if (!document.querySelector('.modal-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop fade show';
            document.body.appendChild(backdrop);

            backdrop.addEventListener('click', () => hideModal(modal));
        }
    }

    function hideModal(modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');

        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.remove();
    }

    function bindCloseActions(modal) {
        // ❌ nút close
        modal.querySelectorAll('.btn-close').forEach(btn => {
            btn.addEventListener('click', () => hideModal(modal));
        });

        // ⌨ ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('show')) {
                hideModal(modal);
            }
        });
    }

    function initRequestQuote() {
        const btn = document.getElementById('btn-request-quote');
        const form = document.getElementById('requestQuoteForm');
        const modal = document.getElementById('requestQuoteModal');

        if (!modal) return;

        bindCloseActions(modal);

        if (btn && !btn.dataset.bound) {
            btn.dataset.bound = '1';
            btn.addEventListener('click', () => showModal(modal));
        }

        if (form && !form.dataset.bound) {
            form.dataset.bound = '1';
            form.addEventListener('submit', function (e) {
                e.preventDefault();

                fetch('/shop/request_quote', {
                    method: 'POST',
                    body: new FormData(form),
                }).then(() => {
                    hideModal(modal);
                    window.location.href = '/thank-you';
                });
            });
        }
    }

    initRequestQuote();
    setTimeout(initRequestQuote, 500);
});
