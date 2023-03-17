function Div(props) {
    return <div>{props.str.map((s) =>
        <h1>{s}</h1>
    )}</div>
}

function getData() {
    axios.get("/message").then(response => {
        let data = response.data;
        ReactDOM.render(<Div str={data} />, document.getElementById("message"));
    })
}


getData();
setInterval(getData, 1000);