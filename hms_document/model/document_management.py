from odoo import models, tools, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class DocumentManagement(models.Model):
    _name = "document.management"

    #images= fields.Many2one(comodel_name="ir.attachment", string="Images") 
    is_document = fields.Binary("Image",
        attachment=True,
        help="Medium-sized image of this contact. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    name = fields.Char(string="Name")
    multi_seq = fields.Integer('Multi Seq')