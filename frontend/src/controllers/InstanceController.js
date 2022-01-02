import { BaseController } from './BaseController.js';
import { FormController } from './FormController.js';
import { InstanceFieldController } from './InstanceFieldController.js';

export class InstanceController extends BaseController {
	rsc_name = 'instances';
	form_ctlr = new FormController(this.token)
	instance_field_ctlr = new InstanceFieldController(this.token)

    api_to_cy_convert([data_api]) {
		let instance_data_cy = {
			data_api: JSON.parse(JSON.stringify(data_api)),
			id: 'instance' + data_api.id,
			class: 'instance',
		};
		let converted_instance_data = {
			group: 'nodes',
			data: instance_data_cy,
			position: { x: 650, y: 150 },
		};
		console.log(`converted instance data`, converted_instance_data);
		return [converted_instance_data];
	}

	async load_instance(instance_id){
		this.instance_data_api = await this.get_rsc_ins(instance_id);
		this.instance_data_cy = this.api_to_cy_convert([this.instance_data_api]);
		
		let form_id = this.instance_data_api.form_id
		this.form_data_api = await this.form_ctlr.get_rsc_ins(form_id);
		this.form_data_cy = this.form_ctlr.api_to_cy_convert([this.form_data_api]);

		this.phases_data_api = await this.form_ctlr.get_rel_rsc(form_id, 'phases');
		this.phases_data_cy = this.form_ctlr.phase_ctlr.api_to_cy_convert(this.phases_data_api);

		this.transitions_data_api = await this.form_ctlr.get_rel_rsc(form_id, 'transitions');
		this.transitions_data_cy = this.form_ctlr.transition_ctlr.api_to_cy_convert(this.transitions_data_api);

		this.sections_data_api = await this.form_ctlr.get_rel_rsc(form_id, 'sections');
		this.sections_data_cy = this.form_ctlr.section_ctlr.api_to_cy_convert(this.sections_data_api, form_id);
		let phase_sections_edges = this.form_ctlr.create_phase_section_edges(this.sections_data_cy);

		this.fields_data_api = await this.form_ctlr.get_rel_rsc(form_id, 'fields');
		this.fields_data_cy = this.form_ctlr.field_ctlr.api_to_cy_convert(this.fields_data_api);

		this.instance_field_data_api = await this.get_rel_rsc(instance_id, 'instances_fields');
		this.instance_field_data_cy = this.instance_field_ctlr.api_to_cy_convert(this.instance_field_data_api);

		let nodes = this.instance_data_cy.concat(
			this.form_data_cy,
			this.sections_data_cy,
			this.phases_data_cy,
			this.fields_data_cy,
			this.instance_field_data_cy
		);
		let edges = this.transitions_data_cy.concat(phase_sections_edges);
		return nodes.concat(edges);
	}
}