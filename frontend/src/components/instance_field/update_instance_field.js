import { useEffect, useState } from "react";
import { useController } from "../../controllers";
import { resizeTextarea } from "../../utils/resize_textarea";

export function UpdateInstanceField ({readonly=true, old_instance_field_data, instances_fields_data, setInstancesFieldsData}) {
    const [value, setValue] = useState(old_instance_field_data.value?old_instance_field_data.value:'')
    const [update, setUpdate] = useState(false);
    const [timeout_id, setTimeoutId] = useState();
    const {InstanceFieldCtlr} = useController();

    async function handleSubmit(e) {
        e.preventDefault();
        const req_bod = {value}
        const data = await InstanceFieldCtlr.patch_rsc_ins(old_instance_field_data.id, req_bod);
        console.log("updated instance field data", data);
        setInstancesFieldsData(instances_fields_data.map(ifsd => ifsd.id == data.id ? data: ifsd))
    }

    useEffect(() => {
        if (update) {
            const req_bod = {value}
            InstanceFieldCtlr.patch_rsc_ins(old_instance_field_data.id, req_bod).then((data) => {
                console.log("updated instance field data", data);
                setInstancesFieldsData(instances_fields_data.map(ifsd => ifsd.id == data.id ? data: ifsd))
            });
        }
        setUpdate(false);
    }, [update])

    useEffect(() => {
        for (const textarea of document.querySelectorAll(".instance-field textarea")){
            resizeTextarea(textarea)
        }
    }, [])

    function handleKeyUp(e) {
        if (readonly) return
        clearTimeout(timeout_id);
        resizeTextarea(e.target)
        setTimeoutId(setTimeout(() => {
            setUpdate(true);
        }, 2000))
    }

    return (
        <div className="instance-field">
            <form onSubmit={handleSubmit}>
                {/* <div className="manage-buttons">
                    <button className="option-button" onClick={e => {
                        e.preventDefault();
						let context_menu = e.target.nextSibling? e.target.nextSibling: e.target.closest(".option-button").nextSibling
						context_menu.classList.toggle("show-options")
					}}>
						<OptionIcon/>
					</button>
                    <div className="context-menu">
                        <div className="option" onSubmit={handleSubmit}>
                            <button type="submit" ><SaveIcon/></button>
                            <span>Save</span>
                        </div>
                        <div className="option"  onClick={cancelSubmit}>
                            <button><CancelIcon/></button>
                            <span>Cancel</span>
                        </div>
                    </div>
                </div> */}

                <textarea name="value" value={value}
                readOnly={readonly}
                onKeyUp={handleKeyUp}
                onChange={e => {
                    setValue(e.target.value);
                }}/>
            </form>
        </div>
    )
}