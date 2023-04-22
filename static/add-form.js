function AddMessageForm() {
    const handleSubmit=(event)=>{
        event.preventDefault();
        const newMessage=event.target.elements.message.value;
        axios.post("/add", {message:newMessage}).then(
            response=>console.log(response.data)
        )
    }
    return (
        <form onSubmit={handleSubmit}>
            Send a message to students<br></br>
            <input class="fill-press" type="text" name="message" autoFocus />
            <input class="fill-press" type="submit" value="Send" />
        </form>
    )
}


ReactDOM.render(<AddMessageForm />, document.getElementById("addForm"));