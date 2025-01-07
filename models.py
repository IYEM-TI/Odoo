# models/loan.py

from odoo import models, fields, api

class Loan(models.Model):
    _name = 'loan.management'
    _description = 'Gestión de préstamos'

    # Campos del préstamo
    name = fields.Char(string='Nombre del Préstamo', required=True)
    amount = fields.Float(string='Monto del Préstamo', required=True)
    interest_rate = fields.Float(string='Tasa de Interés (%)', required=True, help="Porcentaje de interés del préstamo")
    duration = fields.Integer(string='Duración (meses)', required=True)
    start_date = fields.Date(string='Fecha de Inicio', required=True)
    total_amount_due = fields.Float(string='Monto Total a Pagar', compute='_compute_total_amount_due', store=True)
    monthly_payment = fields.Float(string='Pago Mensual', compute='_compute_monthly_payment', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved', 'Aprobado'),
        ('paid', 'Pagado'),
    ], string='Estado', default='draft')

    # Cálculo del monto total a pagar (monto + interés)
    @api.depends('amount', 'interest_rate')
    def _compute_total_amount_due(self):
        for loan in self:
            # El cálculo del monto total es: Monto del préstamo + (Monto * Tasa de interés en porcentaje)
            loan.total_amount_due = loan.amount + (loan.amount * loan.interest_rate / 100)

    # Cálculo del pago mensual (monto total a pagar / duración)
    @api.depends('total_amount_due', 'duration')
    def _compute_monthly_payment(self):
        for loan in self:
            if loan.duration > 0:
                loan.monthly_payment = loan.total_amount_due / loan.duration
            else:
                loan.monthly_payment = 0

    # Método para aprobar el préstamo
    def approve_loan(self):
        self.state = 'approved'

    # Método para marcar como pagado
    def mark_as_paid(self):
        self.state = 'paid'

        
