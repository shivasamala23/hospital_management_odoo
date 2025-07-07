from odoo import models, fields, api, _


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = "Doctors"

    doctor_id=fields.Char(string="Doctor ID", readonly=True,default=lambda self: _('New'))
    name=fields.Char(string="Doctor Name",required=True)
    age=fields.Integer(string="AGE",readonly=True)
    dob=fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    contact_no = fields.Char(string="Contact No")
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'),
         ('o-', 'O-')], string="Blood Group")
    email = fields.Char(string="Email")
    date_of_joining = fields.Datetime(string="Date of Admission", readonly=True, default=fields.Datetime.now)
    doctor_img = fields.Image(string="Image")
    appointments_count = fields.Integer(string="Appointment Count", default=0, compute='_compute_appointments_count')
    specialization = fields.Selection([
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Medicine'),
    ], string="Specialization", required=True)

    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob:
                age = (fields.Date.today() - rec.dob).days // 365.25
                rec.age = age

    @api.model
    def create(self, vals):
        vals['doctor_id'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('NEW')
        return super(Doctor, self).create(vals)

    def write(self, vals):
        res = super(Doctor, self).write(vals)
        return res

    def unlink(self):
        if self:
            self.env.registry.clear_cache()
        return super(Doctor, self).unlink()

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
            rec.appointments_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])

    def open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'calendar,list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {},
            'target': 'current'
        }
    