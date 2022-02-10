import { useState } from "react";
import "./test2.css"

export const Test2 = () => {
    const [text, setText] = useState('')

    const setWidth = function (e) {
        let textboxEle = e.target;
        var length = 0;
        // if (textboxEle.tagName === 'SELECT') {
        //     length = textboxEle.selectedOptions[0].text.length;
        // }
        // else if (textboxEle.tagName === 'INPUT' || textboxEle.tagName === 'TEXTAREA'){
        //     length = textboxEle.value.length;
        // }
        // textboxEle.style.width = length + 1 + 'ch';
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        console.log(textboxEle.style.fontSize, textboxEle.style.fontFamily);
        ctx.font = `${textboxEle.style.fontSize}px ${textboxEle.style.fontFamily}`
        
        var txt = ''
        if (textboxEle.tagName === 'SELECT') {
            txt = textboxEle.selectedOptions[0].text;
        }
        else if (textboxEle.tagName === 'INPUT' || textboxEle.tagName === 'TEXTAREA'){
            txt = textboxEle.value;
        }
        length = ctx.measureText(txt).width;
        textboxEle.style.width = length + 1 + 'px';
    };

  return (
    <div>
        {/* <View style={{backgroundColor: '#000000', alignSelf: 'flex-start' }}>
            <Text style={{color: '#ffffff'}}>
                Sample text here
            </Text>
        </View> */}
        <input type="text" onChange={e => setText(e.target.value)} value={text} onInput={setWidth}></input>
        <select name="" id="" onInput={setWidth}>
            <option value="">Na dep gai</option>
            <option value="">Na dep gai Na dep gai</option>
            <option value="">Na dep gai Na dep gai Na dep gai</option>
        </select>
        <textarea name="" id="" rows="1" value="Some text in" onInput={setWidth} onChange={e => setText(e.target.value)} value={text}></textarea>
        <input type="number" className="" min="1" max="5" value={1} onInput={setWidth}/>
        
        {/* <span class="input" role="textbox" contentEditable>99</span> */}
    </div>
  );
};
