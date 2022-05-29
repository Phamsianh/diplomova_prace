import cytoscape from 'cytoscape'
import dagre from 'cytoscape-dagre'

export function displayPhasesTransitions (container_id, phases_data, transitions_data, instance_data) {
	cytoscape.use(dagre);
	const cy = cytoscape({
		container: document.getElementById(container_id),
		layout: {
			name: 'grid',
			rows: 1
		},
		style: [
			{
				selector: 'node[class = "phase"]',
				style: {
					label: 'data(data_api.name)',
				},
			},
			{
				selector: 'node[class = "current_phase"]',
				style: {
					label: 'data(data_api.name)',
					// 'background-color': 'black',
					"border-width": '2px',
					"border-color": 'black'
				},
			},
			{
				selector: 'edge',
				style: {
					'curve-style': 'bezier',
					'target-arrow-shape': 'triangle',
					'target-arrow-color': 'red',
					'target-endpoint': 'outside-to-node-or-label',
					// label: 'data(data_api.name)',
	
				},
			},
			{
				selector: 'edge[class = "available_transition"]',
				style: {
					'line-color': "green"
				},
			},
		],
	})
	cy.json({elements: convert_phases(phases_data, instance_data).concat(convert_transitions(transitions_data, instance_data))})
	cy.layout({ name: 'dagre' }).run();
		
	return cy;
}

export function convert_phases(phases_data, instance_data) {
	let ph = [];
	if (phases_data !== null && phases_data != [])
		for (const p of phases_data) {
			let phase_data_cy = {
				data_api: JSON.parse(JSON.stringify(p)),
				id: 'phase' + p.id.toString(),
				class: instance_data?.current_phase_id == p.id? 'current_phase': 'phase',
			}
			ph.push({
				group: 'nodes',
				data: phase_data_cy,
				position: { x: 650, y: 150 },
			});
		}
	// console.log(`converted phases data`, ph);
	return ph;
}

export function convert_transitions(transitions_data, instance_data) {
	let tr = [];
	if (transitions_data !== null && transitions_data != [])
		for (const t of transitions_data) {
			let transition_data_cy = {
				data_api: JSON.parse(JSON.stringify(t)),
				id: 'transition' + t.id,
				class: instance_data.current_phase_id == t.from_phase_id? 'available_transition': 'transition',
				source: 'phase' + t.from_phase_id,
				target: 'phase' + t.to_phase_id,
			}
			tr.push({
				group: 'edges',
				data: transition_data_cy
			});
		}
	// console.log(`converted transitions data`, tr);
	return tr;
}

export function displayGroups(container_id, groups_data) {
	cytoscape.use(dagre);
	const cy = cytoscape({
		container: document.getElementById(container_id),
		layout: {
			name: 'grid',
			rows: 1
		},
		style: [
			{
				selector: 'node[class = "group"]',
				style: {
					label: 'data(data_api.name)',
				},
			},
			{
				selector: 'edge',
				style: {
					'curve-style': 'bezier',
					'target-arrow-shape': 'triangle',
					'target-arrow-color': 'red',
					'target-endpoint': 'outside-to-node-or-label',
				},
			},
		],

		layout: {
			name: 'grid',
		}
	})
	cy.json({elements: convert_groups(groups_data)})
	cy.layout({ name: 'dagre' }).run();
		
	return cy;
}

export function convert_groups(groups_data){
	let gr = [];
	if (groups_data !== null && groups_data != [])
		for (const g of groups_data) {
			let group_data_cy = {
				data_api: JSON.parse(JSON.stringify(g)),
				id: 'group' + g.id.toString(),
				class: 'group',
			}
			gr.push({
				group: 'nodes',
				data: group_data_cy,
			});
			if (g.superior_group_id != null){
				let group_connection = {
					id: 'group' + g.id.toString() + 'group' + g.superior_group_id.toString(),
					target: 'group' + g.id.toString(),
					source: 'group' + g.superior_group_id.toString(),
					class: 'connection'
				}
				gr.push({
					group: 'edges',
					data: group_connection,
				})
			}			
		}
	// console.log(`converted groups data`, gr);
	return gr;
}