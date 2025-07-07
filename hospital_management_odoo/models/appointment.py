from odoo import models, fields, api,_
from odoo.exceptions import ValidationError



class Appointment(models.Model):
    _name = "hospital.appointment"
    _rec_name = 'patient_id'
    _description = "Appointment"

    name = fields.Char( related='patient_id.name',string="Name",readonly=True,required=True)
    appointment_id = fields.Char(string="Appointment ID" ,readonly=True,default=lambda self: _('New'))
    date_of_creation = fields.Datetime(string="Date of Creation", default=fields.Datetime.now)
    start_time = fields.Datetime(string="Start Time", required=True)
    end_time = fields.Datetime(string="End Time", required=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient ID")
    patient_img = fields.Image(related='patient_id.patient_img',string="Patient Image")
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    appointment_status = fields.Selection([('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], string="Appointment Status" ,default='pending')

    @api.model
    def create(self, vals):
        vals['appointment_id'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(Appointment, self).create(vals)
        return result

    @api.constrains('doctor_id', 'start_time', 'end_time')
    def _check_doctor_availability(self):
        for rec in self:
            if rec.start_time >= rec.end_time:
                raise ValidationError(_("End time must be after start time."))

            overlapping = self.search([
                ('doctor_id', '=', rec.doctor_id.id),
                ('id', '!=', rec.id),
                ('start_time', '<', rec.end_time),
                ('end_time', '>', rec.start_time),
            ])

            if overlapping:
                raise ValidationError(
                    _("Doctor %s is already booked between %s and %s.") % (
                        rec.doctor_id.name,
                        rec.start_time.strftime('%Y-%m-%d %H:%M'),
                        rec.end_time.strftime('%Y-%m-%d %H:%M')
                    )
                )

