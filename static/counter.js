function Messages(props) {
    const [counter, setCounter] = React.useState([]);
    const getMessages = () => {
        axios.get("/new_message_counter").then((result) => {
            setCounter(result.data);
        })
    }
    React.useEffect(() => {
        getMessages();
        setInterval(getMessages, props.interval);
    }, []
    )
    return (
        <div className='counter'>
            You have {counter} new messages
        </div>
    );
}

ReactDOM.render(<Messages interval={1000} />, document.getElementById("counter"));
