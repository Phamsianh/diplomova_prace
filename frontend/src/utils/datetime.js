export function formatDate(datetime) {
    const now = new Date();
    const time = new Date(datetime)   
    const delta = now - time
    if (delta/(1000) < 60) {
        return 'just now'
    }
    const delta_m = delta/(1000 * 60);
    if (delta_m < 60) {
        return Math.floor(delta_m) + 'm ago'
    }
    const delta_h = delta_m / 60;
    if (delta_h < 24) {
        return Math.floor(delta_h) + 'h ago'
    }
    else {
        return `${time.getHours()}:${time.getMinutes()}, ${time.getDate()}.${time.getMonth()} `
    }
}
