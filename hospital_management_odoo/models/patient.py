from odoo import models, fields, api, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError


class Patient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id'
    _description = 'Patient'

    name = fields.Char(string="Name", required=True, tracking=True)
    patient_id = fields.Char(string="Patient ID", readonly=True, default=lambda self: _('NEW'))
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", readonly=True)
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'),
         ('o-', 'O-')], string="Blood Group")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    contact_no = fields.Char(string="Contact No")
    email = fields.Char(string="Email")
    address = fields.Char(string="Address")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    emergency_contact = fields.Char(string="Emergency Contact")
    patient_img = fields.Image(string="Image")
    appointments_count = fields.Integer(string="Appointment Count", default=0, compute='_compute_appointments_count')
    appointments = fields.Many2one('hospital.appointment')
    date_of_admission = fields.Datetime(string="Date of Admission", readonly=True, default=fields.Datetime.now)
    date_of_discharge = fields.Datetime(string="Date of Discharge")
    type_of_discharge = fields.Selection([('discharged', 'Discharged'), ('expired', 'Expired')],
                                         string="Type of Discharge")
    discharge_reason = fields.Text(string="Discharge Reason")
    discharge_notes = fields.Text(string="Discharge Notes")
    reason_for_visit = fields.Text(string="Reason for Visit")
    expired_date = fields.Datetime(string="Expired Date")
    expired_reason = fields.Text(string="Expired Reason")


    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob:
                age = (fields.Date.today() - rec.dob).days // 365.25
                rec.age = age

    @api.model
    def create(self, vals):
        vals['patient_id'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('NEW')
        return super(Patient, self).create(vals)

    def write(self, vals):
        res = super(Patient, self).write(vals)
        return res

    def unlink(self):
        if self:
            self.env.registry.clear_cache()
        return super(Patient, self).unlink()

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if rec.name:
                if len(rec.name) < 3:
                    raise models.ValidationError(_("Name should be at least 3 characters long"))

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                if not '@' in rec.email:
                    raise models.ValidationError(_("Email should be in the format <EMAIL>"))

    @api.constrains('contact_no')
    def _check_contact_no(self):
        for rec in self:
            if rec.contact_no:
                if len(rec.contact_no) != 10:
                    raise models.ValidationError(_("Contact number should be 10 digits long"))

    def _compute_appointments_count(self):
        for rec in self:
            rec.appointments_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    def open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {},
            'target': 'current'
        }
