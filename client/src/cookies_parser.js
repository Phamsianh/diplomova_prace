const get_cookie = (key) => {
    var value = '';
    var cookies = decodeURIComponent(document.cookie).split('; ');

    for (let i = 0; i < cookies.length; i++) {
        // cookies[i] = cookies[i].trim();
        if(cookies[i].indexOf(key) == 0){
            value = cookies[i].substring(key.length+1)
            return value;
        }
    }
    return '';
}

const delete_cookie = (key) => {
    console.log( key + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/');
    document.cookie = key + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
}
 
export {get_cookie, delete_cookie};