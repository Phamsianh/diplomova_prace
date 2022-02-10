import { adecrypt } from '../utils/crypt.js';
import { BaseController } from './BaseController.js';

export class CommitController extends BaseController {
	rsc_name = 'commits';
	
	convertEnvelopeToContent(envelopes, akey='superstrongkey') {
		return envelopes.map(e => {
			return {
				field_id: e.field_id,
				hash_envelope: e.hash_envelope.substring(0,4),
				value: adecrypt(e.encrypted_content, akey),
				resolved: e.resolved
			}
		});	
	}
}
