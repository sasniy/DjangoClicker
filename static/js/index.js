function call_click() {
    fetch('/call_click/', {
        method: 'GET'
    }).then(response => {

        if (response.ok) {
            return response.json()
        }

        return Promise.reject(response)
    }).then(data => {
        if(data.is_levelup)
        {
            get_boosts()
       }
        document.getElementById('coins').innerText = data.core.coins
    }).catch(error => console.log(error))
   }
function buy_boost(boost_id) {
    fetch('/buy_boost/' + boost_id, {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
        document.getElementById('click_power').innerText = data.core.click_power
    }).catch(error => console.log(error))
}
function get_boosts() {
    fetch('/boosts/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(boosts => {
        const panel = document.getElementById('boosts-holder')
        panel.innerHTML = ''
        boosts.forEach(boost => {
            add_boost(panel, boost)
        })
    }).catch(error => console.log(error))
}
function add_boost(parent, boost) {
    const button = document.createElement('button')
    button.setAttribute('class', 'boost')
    button.setAttribute('id', `boost_${boost.id}`)
    button.setAttribute('onclick', `buy_boost(${boost.id})`)
    button.innerHTML = `
        <p>lvl <span id = 'boost_id'>${boost.id}</span></p>
        <p>+<span id="boost_power">${boost.power}</span></p>
        <p><span id="boost_price">${boost.price}</span></p>
    `
    parent.appendChild(button)
}