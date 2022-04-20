import { adecrypt } from '../utils/crypt.js';
import { BaseController } from './BaseController.js';

export class CommitController extends BaseController {
	rsc_name = 'commits';
	
	convertEnvelopeToContent(envelopes, instances_fields_data) {
		return envelopes.map(e => {
			let field_id = instances_fields_data.find(ifd => ifd.id == e.instance_field_id).field_id
			return {
				id: e.instance_field_id,
				field_id: field_id,
				creator_id: e.creator_id,
				hash_envelope: e.hash_envelope.substring(0,4),
				value: e.content_value,
				updated_at: e.updated_at
			}
		});	
	}
}
