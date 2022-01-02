export function sencrypt(value, skey) {
    return 'encryptedwith_' + skey + value;
}

export function sdecrypt(value, skey){
    return value.replace('encryptedwith_' + skey, '');
}

export function aencrypt(value, akey) {
    return 'encryptedwith_' + akey + value;
}

export function adecrypt(value, akey) {
    return value.replace('encryptedwith_' + akey, '');
}

export function hash(value) {
    
}

export function sign(value) {
    return 'signed_' + value;
}