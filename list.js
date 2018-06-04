let t = document.getElementsByClassName('transaction-row');
let ar = [];

for (let i=1; i<t.length; i++) {
    let k = t[i];
    let name = k.childNodes[1].childNodes[1].childNodes[1].firstChild.data;
    let url = k.childNodes[3].childNodes[1].childNodes[1].href;
    ar.push({'neighbourhood':name.trim(), 'url': url});
}