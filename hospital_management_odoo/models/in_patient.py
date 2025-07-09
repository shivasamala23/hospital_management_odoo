# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields,models,api,_


class InPatient(models.Model):

    _name='in.patient'
    _inherit = ['mail.thread']

    admission_id=fields.Char(string="Admission ID",readonly=True,default=lambda self:_('New'))
    name=fields.Char(related="patient_id.name",string="Patient Name",readonly=True)
    patient_id=fields.Many2one('hospital.patient',string="Patient ID")
    admission_date=fields.Datetime(string="Admission Date",default=fields.Datetime.now,readonly=True)
    discharge_date=fields.Datetime(string="Discharge Date")
    doctor_id=fields.Many2one('hospital.doctor')

    @api.model
    def create(self,vals):
        vals['admission_id']=self.env['ir.sequence'].next_by_code('in.patient') or _('New')
        return super(InPatient,self).create(vals)
    def write(self, vals):
        return super(InPatient,self).write(vals)
    def unlink(self,vals):
        return super(InPatient,self).unlink(vals)
