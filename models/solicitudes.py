# models/solicitudes.py
from odoo import models, fields, api

class SolicitudPrestamo(models.Model):
    _name = 'prestamos.solicitud'
    _description = 'Solicitud de Préstamo'

    # Campos del modelo
    clave_contrato = fields.Char(string="Clave de Contrato", required=True)
    folio_contrato = fields.Char(string="Folio de Contrato", required=True)
    cliente_id = fields.Many2one('res.partner', string='Acreditado', required=True)
    monto_otorgado = fields.Monetary(string="Monto Otorgado", required=True)
    tipo_credito = fields.Selection([
        ('artesanal', 'Artesanal'),
        ('emprendedores', 'Emprendedores'),
        ('sustentable', 'Sustentable')
    ], string="Tipo de Crédito", required=True)
    plazo = fields.Selection([('12', '12 meses'), ('18', '18 meses'), ('24', '24 meses')], string="Plazo de Devolución", required=True)
    tasa_interes = fields.Float(string="Tasa de Interés Anual", compute='_compute_tasa_interes', store=True)
    tasa_interes_moratorio = fields.Float(string="Tasa de Interés Moratorio", compute='_compute_tasa_interes_moratorio', store=True)
    fecha_entrega = fields.Date(string="Fecha de Entrega", default=fields.Date.today)
    estatus = fields.Selection([('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('en_pago', 'En Pago'), ('pagado', 'Pagado')], string="Estatus", default='pendiente')
    tabla_amortizacion = fields.One2many('prestamos.amortizacion', 'solicitud_id', string="Tabla de Amortización")

    @api.depends('tipo_credito')
    def _compute_tasa_interes(self):
        for record in self:
            if record.tipo_credito == 'artesanal':
                record.tasa_interes = 7  # Por ejemplo, 7% para mujeres, puedes incluir lógica aquí según sexo
            elif record.tipo_credito == 'emprendedores':
                record.tasa_interes = 7  # Igual que artesanal
            elif record.tipo_credito == 'sustentable':
                record.tasa_interes = 5  # 5% para sustentable

    @api.depends('tasa_interes')
    def _compute_tasa_interes_moratorio(self):
        for record in self:
            record.tasa_interes_moratorio = record.tasa_interes * 2.5  # Moratorio es 2.5 veces la tasa ordinaria

    @api.model
    def create(self, vals):
        record = super(SolicitudPrestamo, self).create(vals)
        record._generar_tabla_amortizacion()
        return record

    def _generar_tabla_amortizacion(self):
        # Lógica para generar la tabla de amortización
        for record in self:
            # El monto fijo sería el monto dividido entre el número de pagos según el plazo
            monto_fijo = record.monto_otorgado / int(record.plazo) 
            for mes in range(1, int(record.plazo) + 1):
                self.env['prestamos.amortizacion'].create({
                    'solicitud_id': record.id,
                    'mes': mes,
                    'monto_pago': monto_fijo,
                    'interes_ordinario': monto_fijo * (record.tasa_interes / 100),
                    'capital': monto_fijo * (1 - (record.tasa_interes / 100)),
                    'fecha_pago': fields.Date.add(record.fecha_entrega, months=mes),
                })
