# -- encoding: utf-8 --

from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class PersonalNote(models.Model):
    _name = 'personal.note'
    _description = 'Personal Note for users'
    
    # ------------------------------------------------------
    # DEFAULT METHODS
    # ------------------------------------------------------
    @api.model
    def archive_old_notes(self):
        """Marca como no importantes las notas de hace más de 30 días"""
        limit_date = datetime.today() - timedelta(days=30)
        old_notes = self.search([('date', '<=', limit_date.date()), ('important', '=', True)])
        old_notes.write({'important': False})
        _logger = self.env['ir.logging']
        _logger.create({
            'name': 'Notas archivadas',
            'type': 'server',
            'level': 'INFO',
            'dbname': self._cr.dbname,
            'message': f'Se marcaron {len(old_notes)} notas como no importantes.',
            'path': __name__,
            'func': 'archive_old_notes',
            'line': 0,
        })
    # ------------------------------------------------------
    # COMPUTE AND INVERSE METHODS
    # ------------------------------------------------------
    @api.depends('important')
    def _compute_important_text(self):
        for record in self:
            record.important_text = 'Importante' if record.important else 'No importante'
            
    def _compute_description_short(self):
        for rec in self:
            rec.description_short = (rec.description[:25] + '...') if rec.description and len(rec.description) >25 else rec.description
    # ------------------------------------------------------
    # SELECTION METHODS
    # ------------------------------------------------------
    # ------------------------------------------------------
    # CONSTRAINTS AND VALIDATIONS
    # ------------------------------------------------------
    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name) < 5:
                raise ValidationError(_("El título de la nota debe tener como mínimo 5 caracteres."))
    # ------------------------------------------------------
    # ONCHANGE METHODS
    # ------------------------------------------------------
    # ------------------------------------------------------
    # CRUD METHODS
    # ------------------------------------------------------
    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------
    def action_toggle_important(self):
        self.ensure_one()
        self.important = not self.important
        message = (
            "Nota marcada como importante." if self.important
            else "Nota desmarcada como importante."
        )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Estado actualizado',
                'message': message,
                'sticky': False,
                'type': 'success',
            }
        }
        
    
    def print_report(self):
        return self.env.ref('personal_notes.action_report_personal_note').report_action(self)
    
    # ------------------------------------------------------
    # OTHER BUSINESS METHODS
    # ------------------------------------------------------
    # ------------------------------------------------------
    # COLUMNS
    # ------------------------------------------------------
    name = fields.Char(
        string='Título',
        required=True,
        help='Título de la nota',
    )
    description = fields.Text(
        string='Descripción',
        help='Descripción de la nota',
    )
    description_short = fields.Char(
        compute='_compute_description_short'
    )
    date = fields.Date(
        string='Fecha',
        help='Fecha planificada de la nota',
    )
    important = fields.Boolean(
        string='Marcar como importante',
        help='Marcar la nota como importante',
    )
    user_id = fields.Many2one(
        'res.users', 
        string='Usuario', 
        default=lambda self: self.env.user,
    )
    important_text = fields.Char(
        string='Estado marcado como importante',
        compute='_compute_important_text'
    )
    personal_note_count = fields.Integer(
        string='Notas', 
        compute='_compute_personal_note_count'
    )    
    partner_id = fields.Many2one(
        'res.partner', 
        string='Contacto'
    )
    color = fields.Integer("Color")
