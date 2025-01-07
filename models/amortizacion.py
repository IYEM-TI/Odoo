# models/amortizacion.py
from odoo import models, fields

class Amortizacion(models.Model):
    _name = 'prestamos.amortizacion'
    _description = 'Tabla de Amortización'

    solicitud_id = fields.Many2one('prestamos.solicitud', string="Solicitud de Préstamo", required=True)
    fecha_vencimiento = fields.Date(string="Fecha de Vencimiento", required=True)
    monto_capital = fields.Monetary(string="Capital", required=True)
    monto_interes_ordinario = fields.Monetary(string="Interés Ordinario", required=True)
    monto_interes_moratorio = fields.Monetary(string="Interés Moratorio", required=True, default=0.0)
    monto_pago = fields.Monetary(string="Monto a Pagar", required=True)
    estatus = fields.Selection([('pendiente', 'Pendiente'), ('pagado', 'Pagado')], string="Estatus", default='pendiente')

    # Este campo se puede usar para actualizar la tabla de amortización cuando se haga un pago
    pago_id = fields.Many2one('prestamos.pago', string="Pago Asociado")
