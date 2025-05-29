# -- encoding: utf-8 --

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'


    def _compute_note_count(self):
        for partner in self:
            partner.note_count = self.env['personal.note'].search_count([
                ('partner_id', '=', partner.id)
            ])       
            
    
    note_count = fields.Integer(
        string='Notas', 
        compute='_compute_note_count'
    )