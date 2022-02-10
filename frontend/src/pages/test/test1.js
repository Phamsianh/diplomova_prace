import React from 'react'
import { CommitsPageIcon, CreateIcon, OptionIcon, PrintPDFIcon, SaveIcon } from '../../components/icon'
import './main.css'
export const Test1 = () => {
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
                    <label>
                        First name
                        <textarea disabled name="" id="first-name" cols="30" rows="1"></textarea><br />
                    </label>
                    <label>
                        Last name
                        <textarea name="" id="" cols="30" rows="10"></textarea>
                    </label>

                    <div className="new-field">
                        <form>
                            <label>
                                field name
                                <input type="text" name="field-name" id="field-name" />
                            </label>
                            <label>
                                order
                                <input type="number" name="order" id="order" min="1" max="5" />
                            </label>
                            <button type="submit"><SaveIcon/></button>
                        </form>
                    </div>
                    <button><CreateIcon/></button>
                </div>
                <div className="new-section section">
                    <form>
                        <label>
                            section name
                            <input type="text"></input>
                        </label>
                        <label>
                            position
                            <select name="position" id="position">
                                <option value="1">Student of CIT</option>
                            </select>
                        </label>
                        <label>
                            order
                            <input type="number" name="order" id="order" min="1" max="5" />
                        </label>
                        <button type="submit"><SaveIcon/></button>
                    </form>
                </div>
                <button><CreateIcon/></button>
                <div className="phase-name">
                    <span><i>Phase's name</i></span>
                </div>
            </div>
            <hr />
            
            <div className="phase">
                <div className="section">
                    <h4 className="section-name">Leadding Teacher section</h4>
                    <label>
                        First name
                        <textarea name="" id="" cols="30" rows="1"></textarea>
                    </label><br />

                    <label>
                        Last name
                        <textarea name="" id="" cols="30" rows="1"></textarea>                
                    </label>
                </div>

                <div className="section">
                    <h4 className="section-name">Consultant section</h4>

                    <label>First name
                        <textarea name="" id="" cols="30" rows="1"></textarea>
                    </label><br />

                    <label>Last name
                        <textarea name="" id="" cols="30" rows="1"></textarea>
                    </label>
                </div>
                <div className="phase-name">
                    <span><i>Phase name</i></span>
                </div>    
            </div>
            <hr />

            <div className="new-phase phase">
                <form>
                    <label>
                        phase name
                        <input type="text"></input>
                    </label>
                    <label>
                        director
                        <select name="position-id">
                            <option value="1">Pham Si Anh</option>
                        </select>
                    </label>
                    <label>
                        phase type
                        <select name="phase-type" id="phase-type">
                            <option value="begin">begin</option>
                            <option value="transit">transit</option>
                            <option value="end">end</option>
                        </select>
                    </label>
                    <label>
                        description
                        <input type="text"/>
                    </label>
                    <button><SaveIcon/></button>
                </form>
            </div>
            <button><CreateIcon/></button>
        </div>
    )
}
