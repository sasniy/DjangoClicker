

function call_click() {
    var audio = new Audio('media/sounds/Spank.mp3')
    audio.play()

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
            var boost_audio = new Audio('media/sounds/new_boosts.mp3')
            boost_audio.play()
            document.getElementById('next_boost').innerText = data.next_boost
       }
        document.getElementById('coins').innerText = data.core.coins
    }).catch(error => console.log(error))
   }
function buy_boost(boost_id) {
    fetch('/buy_boost/' + boost_id, {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            var audio = new Audio('media/sounds/buy_boost.mp3')
            audio.play()
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
        document.getElementById('click_power').innerText = data.core.click_power
        document.getElementById('next_boost').innerText = data.price
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