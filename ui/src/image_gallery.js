import React, { Component } from "react";

class ImageGal extends Component {
  render() {
    if (this.props.result) {
        let res = [];
        Object.keys(this.props.result).forEach(element => {
            res.push(<h2>{element}</h2>);
            this.props.result[element].forEach(e => {
                res.push(<div><img src={e}/></div>);
            });
        });

      return (
      <div>
      {res}
      </div>);
    } else if(this.props.jobRunning) {
      return <div> loading... </div>;
    } else {
        return <div></div>;
    }
  }
}

export default ImageGal;
