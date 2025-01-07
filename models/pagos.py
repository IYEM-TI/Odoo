# models/pagos.py
from odoo import models, fields, api
from datetime import timedelta

class Pago(models.Model):
    _name = 'prestamos.pago'
    _description = 'Registro de Pago'

    solicitud_id = fields.Many2one('prestamos.solicitud', string="Solicitud de Préstamo", required=True)
    fecha_pago = fields.Date(string="Fecha de Pago", required=True)
    monto_pago = fields.Monetary(string="Monto del Pago", required=True)
    tipo_pago = fields.Selection([('efectivo', 'Efectivo'), ('transferencia', 'Transferencia')], string="Tipo de Pago", required=True)
    interes_condonado = fields.Boolean(string="Condonar Interés", default=False)
    interes_moratorio_condonado = fields.Boolean(string="Condonar Interés Moratorio", default=False)
    capital_pagado = fields.Monetary(string="Monto Capital Pagado", compute="_compute_detalles_pago")
    interes_ordinario_pagado = fields.Monetary(string="Interés Ordinario Pagado", compute="_compute_detalles_pago")
    interes_moratorio_pagado = fields.Monetary(string="Interés Moratorio Pagado", compute="_compute_detalles_pago")

    @api.depends('monto_pago', 'solicitud_id')
    def _compute_detalles_pago(self):
        for pago in self:
            solicitud = pago.solicitud_id
            monto_pago_restante = pago.monto_pago

            # Cálculo de lo que corresponde a Capital y el interés ordinario
            if not pago.interes_condonado:
                pago.interes_ordinario_pagado = monto_pago_restante * (solicitud.tasa_interes / 100)
                monto_pago_restante -= pago.interes_ordinario_pagado

            # Cálculo del interés moratorio si aplica
            if not pago.interes_moratorio_condonado:
                pago.interes_moratorio_pagado = monto_pago_restante * (solicitud.tasa_interes_moratorio / 100)
                monto_pago_restante -= pago.interes_moratorio_pagado

            # El resto se destina a Capital
            pago.capital_pagado = monto_pago_restante

            # Actualizamos la tabla de amortización
            self._actualizar_tabla_amortizacion(pago, monto_pago_restante)

    def _actualizar_tabla_amortizacion(self, pago, monto_pago_restante):
        # Aquí actualizamos la tabla de amortización con el pago realizado
        for fila in pago.solicitud_id.tabla_amortizacion:
            if fila.monto_pago > 0:
                if fila.monto_pago <= monto_pago_restante:
                    fila.monto_pago = 0  # Se paga todo
                    monto_pago_restante -= fila.monto_pago
                else:
                    fila.monto_pago -= monto_pago_restante  # Solo se paga parcialmente
                    monto_pago_restante = 0
            if monto_pago_restante == 0:
                break
