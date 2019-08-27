const BASE_URL = 'http://localhost:5000';
const $CAKE_LIST = $('#cupcakes-list');
const $NEW_CUP_FORM = $('#new-cup-form');
const $SEARCH_FORM = $('#search-form');
const $SEARCH_FLAVOR = $('#search-flavor');

$(async function() {

    await addCupcakesToList();

    async function getCupcakes(){
        let response = await axios.get(`${BASE_URL}/api/cupcakes`);
        let cupcakes = response.data.cupcakes.map(cup => ({flavor: cup.flavor, size: cup.size, rating: cup.rating, image: cup.image}));
        return cupcakes;
    };

    function addOneCupcake(cup){
        return (
            `<div.card class="d-inline-block border">
                <img src=${cup.image} class="card-img-top" style="width: 15rem">
                <div class="card-body">
                    <h5 class="card-title">${cup.flavor}</h5>
                    <p class="card-text">Rating = ${cup.rating} Size = ${cup.size}</p>
                </div>
            </div>`)
    };

    async function addCupcakesToList(){
        let cupcakes = await getCupcakes();
        for (cup of cupcakes) {
            $CAKE_LIST.append(addOneCupcake(cup));
        }
    };

    $NEW_CUP_FORM.on("submit", async function (e) {
        e.preventDefault();
        let flavor = $("#flavor").val();
        let size = $("#size").val();
        let rating = $("#rating").val();
        let image = $("#image").val();

        let response = await axios.post(`${BASE_URL}/api/cupcakes`, {
            flavor, size, rating, image});
        $CAKE_LIST.append(addOneCupcake(response.data.cupcake));
        $NEW_CUP_FORM.trigger("reset");
    });

    $SEARCH_FORM.on("submit", async function (e) {
        e.preventDefault();
        let flavor = $SEARCH_FLAVOR.val()
        let response = await axios.get(`${BASE_URL}/api/cupcakes`, {params: {
            flavor: flavor
        }});
        $CAKE_LIST.empty();
        for (cup of response.data.cupcakes) {
            $CAKE_LIST.append(addOneCupcake(cup));
        }
        $SEARCH_FORM.trigger("reset");
    });

})