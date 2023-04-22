function Messages(props) {

    const [message, setMessage] = React.useState([]);
    const [index, setIndex] = React.useState(0);

    const getMessages = () => {
        axios.get("/updates").then(result => {
            setMessage(result.data);
        })
    }

    React.useEffect(() => {
        getMessages();
        setInterval(getMessages, props.interval);
        setInterval(() => setIndex(index => index + 1), 3000)
    }, []
    )

    return (
        <div>
            <div>{index < 5 ? message[index] : setIndex(0)}</div>
        </div>
    );
}

ReactDOM.render(<Messages interval={10000} />, document.getElementById("message"));