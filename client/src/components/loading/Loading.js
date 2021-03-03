const Loading = (prop) => {
    return (
        <div className="loading display-flex flex-center width-100 height-100">
            {prop.content}
        </div>
    );
}
 
export default Loading;