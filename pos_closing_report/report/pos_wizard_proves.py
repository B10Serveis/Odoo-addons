# -*- coding: utf-8 -*-

import datetime
import pytz
import time
from odoo import api, fields, models


class Reportposreportclosing(models.AbstractModel):
    _name = 'report.pos_closing_report.pos_closing_report'

    @api.model
    def get_session(self, date_ini=False, date_fi=False, config_id=False):
    
        if not config_id:
            config_id = self.env['pos.session'].search([])
        
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
        today = today.astimezone(pytz.timezone('UTC'))
        if date_ini:
            date_ini = fields.Datetime.from_string(date_ini)
        else:
            date_ini = today

        if date_fi:
            date_fi = fields.Datetime.from_string(date_fi)
        else:
            date_fi = today + timedelta(days=1, seconds=-1)

        date_fi = max(date_fi, date_ini)

        date_ini = fields.Datetime.to_string(date_ini)
        date_fi = fields.Datetime.to_string(date_fi)
                
        session_ids = self.env['account.bank.statement'].search([
            ('create_date', '>=', date_ini),
            ('create_date', '<=', date_fi)])
            
        name_pos = self.env["pos.config"].search([('id', '=', config_id)]).name
        
#        session_bank = self.env['account.bank.statement'].search([])
#        amount = {}
#        for payment in session_bank:
#            amount.setdefault(payment.pos_session_id, 0.0)
#            amount[payment.pos_session_id] += payment.balance_end
#            if payment.pos_session_id in amount:
#               amountanterior = amount[payment.pos_session_id]
#            else:
#               amountanterior = 0
#            amount[payment.pos_session_id] = payment.balance_end + amountanterior
        
        return {
            'ident': config_id,
            'name': name_pos,
            'date_ini': date_ini,
            'date_fi': date_fi,
            'sessions': [{
                'session_id': session.pos_session_id.id,
                'session_name': session.pos_session_id.name,
                'session_stat': session.pos_session_id.state,
                'session_ini': session.pos_session_id.start_at,
                'session_fi': session.pos_session_id.stop_at,
                'session_amount': session.balance_end
                } for session in session_ids]
            } 
        
    @api.multi
    def render_html(self, docids, data=None):
        data = dict(data or {})
        config_id = self.env['pos.config'].browse(data['session_id'])
        data.update(self.get_session(data['date_start'], data['date_stop'], data['session_id']))
        return self.env['report'].render('pos_closing_report.pos_closing_report', data)

