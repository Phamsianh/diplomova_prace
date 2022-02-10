export function resizeTextarea (ele) {
    ele.style.height = "3em";
    let computed_style = getComputedStyle(ele);
    let border_bottom = computed_style.borderBottomWidth // in px
    let border_top = computed_style.borderTopWidth  // in px
    border_top = Number(border_top.substring(0, border_top.length - 2))
    border_bottom = Number(border_bottom.substring(0, border_bottom.length - 2))
    let textarea_extended_height = ele.scrollHeight + border_top + border_bottom;
    ele.style.height = textarea_extended_height + "px";
}