import React from 'react'
import { CommitsPageIcon, CreateIcon, OptionIcon, PrintPDFIcon } from '../../components/icon'
import './main.css'
export const Test = () => {
    return (
        <div className='form-container'>
            <div className="manage-buttons">
                <button><OptionIcon/></button>
                <button><PrintPDFIcon/></button>
            </div>
            <h1>Ten form</h1>
            
            <div className="phase">
                <div className="section">
                    <h4>Student of CIT section - User's name</h4>
                    <input type="checkbox" name="" id="" />
                    <label>
                        First name
                        <textarea disabled name="" id="first-name" cols="30" rows="1"></textarea><br />
                    </label>
                    <input disabled type="checkbox" name="" id="" />
                    <label>
                        Last name
                        <textarea name="" id="" cols="30" rows="10"></textarea>
                    </label>
                </div>
                <div className="phase-name">
                    <span><i>Phase's name</i></span>
                </div>
            </div>
            
            <div className="phase">
                <div className="section">
                    <h4 className="section-name">Leadding Teacher section</h4>
                    <span>
                        <input type="checkbox" name="" id="" />
                    </span>
                    <label>
                        First name
                        <textarea name="" id="" cols="30" rows="1"></textarea>
                    </label><br />
                    <span>
                        <input type="checkbox" name="" id="" />
                    </span>

                    <label>
                        Last name
                        <textarea name="" id="" cols="30" rows="1"></textarea>                
                    </label>
                </div>

                <div className="section">
                    <h4 className="section-name">Consultant section</h4>
                    <span>
                        <input type="checkbox" name="" id="" />
                    </span>

                    <label>First name
                        <textarea name="" id="" cols="30" rows="1"></textarea>
                    </label><br />
                    
                    <span>
                        <input type="checkbox" name="" id="" />
                    </span>

                    <label>Last name
                        <textarea name="" id="" cols="30" rows="1"></textarea>
                    </label>
                </div>
                <div className="phase-name">
                    <span><i>Phase name</i></span>
                </div>    
            </div>
        </div>
    )
}
