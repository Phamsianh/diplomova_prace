import domain from "../config.js"

export class BaseController{
    domain = domain
    rsc_name = ''
    AbortCtlr = new AbortController()

    constructor(token){
        this.token = token;
    }
    
    async get_rsc_col() {
        const url = `${domain}/${this.rsc_name}`
        const resp = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: {
                Authorization: `Bearer ${this.token}`,
            },
            signal: this.AbortCtlr.signal
        }).catch((e) => console.error('GET FETCH ERROR', e));
    
        // handle the response status
        if (resp.status !== 200) {
            let error_detail = await resp.json();
            throw new Error(JSON.stringify(error_detail));
        } else return resp.json();
    }

    async get_rsc_ins(rsc_id) {
        const url = `${domain}/${this.rsc_name}/${rsc_id}`
        const resp = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: {
                Authorization: `Bearer ${this.token}`,
            },
            signal: this.AbortCtlr.signal
        }).catch((e) => console.error('GET FETCH ERROR', e));
    
        // handle the response status
        if (resp.status !== 200) {
            let error_detail = await resp.json();
            throw new Error(JSON.stringify(error_detail));
        } else return resp.json();
    }

    async get_rel_rsc(rsc_id, rel_rsc) {
        const url = `${domain}/${this.rsc_name}/${rsc_id}/${rel_rsc}`
        const resp = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: {
                Authorization: `Bearer ${this.token}`,
            },
            signal: this.AbortCtlr.signal
        }).catch((e) => console.error('GET FETCH ERROR', e));
    
        // handle the response status
        if (resp.status !== 200) {
            let error_detail = await resp.json();
            throw new Error(JSON.stringify(error_detail));
        } else return resp.json();
    }
    
    async post_rsc(req_bod) {
        const url = `${domain}/${this.rsc_name}` 
        const resp = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            headers: {
                Authorization: `Bearer ${this.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req_bod),
            signal: this.AbortCtlr.signal
        }).catch((e) => console.error('POST FETCH ERROR', e));
    
        // handle the response status
        if (resp.status !== 200) {
            let error_detail = await resp.json();
            throw new Error(JSON.stringify(error_detail));
        } else return resp.json();
    }
    
    async patch_rsc_ins(rsc_id, req_bod) {
        const url = `${domain}/${this.rsc_name}/${rsc_id}`
        const resp = await fetch(url, {
            method: 'PATCH',
            mode: 'cors',
            headers: {
                Authorization: `Bearer ${this.token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req_bod),
            signal: this.AbortCtlr.signal
        }).catch((e) => console.error('PUT FETCH ERROR', e));
    
        // handle the response status
        if (resp.status !== 200) {
            let error_detail = await resp.json();
            throw new Error(JSON.stringify(error_detail));
        } else return resp.json();
    }
    
    async delete_rsc_ins(rsc_id) {
        const url = `${domain}/${this.rsc_name}/${rsc_id}`
        const resp = await fetch(url, {
            method: 'DELETE',
            mode: 'cors',
            headers: {
                Authorization: `Bearer ${this.token}`,
                'Content-Type': 'application/json',
            },
            signal: this.AbortCtlr.signal
        }).catch((e) => console.error('DELETE FETCH ERROR', e));
    
        // handle the response status
        if (resp.status !== 410) {
            let error_detail = await resp.json();
            throw new Error(JSON.stringify(error_detail));
        } else return resp.json();
    }
}