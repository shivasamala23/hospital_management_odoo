from odoo import models, fields, api,_



class Appointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['hospital.patient']
    _rec_name = 'patient_id'
    _description = "Appointment"

    name = fields.Char( related='patient_id.name',string="Name",readonly=True,required=True)
    appointment_id = fields.Char(string="Appointment ID" ,readonly=True,default=lambda self: _('New'))
    date_of_creation = fields.Datetime(string="Date of Creation", default=fields.Datetime.now)
    appointment_date = fields.Datetime(string="Appointment Date", required=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient ID")
    patient_img = fields.Image(related='patient_id.patient_img',string="Patient Image")
    # doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    appointment_status = fields.Selection([('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], string="Appointment Status" ,default='pending')

    @api.model
    def create(self, vals):
        vals['appointment_id'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(Appointment, self).create(vals)
        return result

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.patient_id} - {record.name}"
            result.append((record.id, name))
        return result