import React, { useState, useEffect } from 'react';
import * as d3 from "d3";
import 'bootstrap/dist/css/bootstrap.css';

// citation: https://embed.plnkr.co/plunk/WjmCzZ 

// draw all bars 
class Bar extends React.Component {

    constructor(props) {
    super(props)
    }

    render() {
    let style = {
        fill: "steelblue"
    }

    return(
        <g>
            <rect className="bar" style={style} x={this.props.x} y={this.props.y + 80} width={this.props.width} height={this.props.height - 194} />
        </g>
    )
    }

}

// draw y-axis 
class YAxis extends React.Component {

    constructor(props) {
    super(props)
    }

    render() {
    let style = {
        stroke: "steelblue",
        strokeWidth: "1px"
    }
    
    let textStyle = {
        fontSize: "0.8em",
        fill: "steelblue",
        textAnchor: "end"
    }
    
    let ticks = d3.range(-40, this.props.end, (this.props.end / this.props.labels.length) + 4)
    
    let lines = []
    ticks.forEach((tick, index) => {
        lines.push(<line style={style} y1={tick} x1={this.props.y} y2={tick} x2={this.props.y - 4}  />)
    })
    
    let columnLables = []
    ticks.forEach((tick, index) => {
        columnLables.push(<text style={ textStyle } y={tick + 5} x={this.props.y - 7} fontFamily="Verdana">{this.props.labels[index]}</text>)
    })
    
    
    return(
        <g>
            <g className="y_labels" transform={`translate(${-5},${17})`}>
            <line x1={this.props.y} y1={this.props.start} y2={this.props.end} x2={this.props.y} style={ style } />
            </g>
            <g className="y_labels" transform={`translate(${-5},${51})`}>
            { columnLables }
            { lines }
            </g>
        </g>
    )
    }

}

// draw x-axis 
class XAxis extends React.Component {
    constructor(props) {
    super(props)
    }

    render() {
    let style = {
        stroke: "steelblue",
        strokeWidth: "1px"
    }
    
    let step = ((this.props.end + this.props.start) / this.props.labels.length)

    let ticks = d3.range(this.props.start, this.props.end, step)
    
    let lines = []
    ticks.forEach((tick, index) => {
        lines.push(<line style={style} x1={tick + 10} y1={this.props.x} x2={tick + 10} y2={this.props.x + 4}  />)
    })
    
    let columnLables = []
    ticks.forEach((tick, index) => {
        columnLables.push(<text style={{fill: "steelblue", "text-anchor": "end"}} transform={`translate(${tick+10},${this.props.x+10})rotate(-75)`} fontFamily="Verdana" fontSize="12">{this.props.labels[index]}</text>)
    })
    
    
    return(
        <g>
            <line x1={this.props.start} y1={this.props.x } x2={this.props.end} y2={this.props.x} style={ style } />
            { columnLables }
            { lines }
        </g>
    )
    }

}

// putting it all together: bars, y-axis, x-axis 
class BarChart extends React.Component {

    render() {
        let data = this.props.data
    
        let margin = {top: 20, right: 20, bottom: 30, left: 45},
            width = 800 - margin.left - margin.right,
            height = 600 - margin.top - margin.bottom;

        let xlabs; 
    
        if (this.props.bookOrAuthor === true) {
            xlabs = data.map((d) => d.title)
        } else {
            xlabs = data.map((d) => d.name)
        }
       
        let ticks = d3.range(0, width, (width / data.length))
        let x = d3.scaleOrdinal()
            .domain(xlabs)
            .range(ticks)
        let y = d3.scaleLinear()
            .domain([0, 5])
            .range([height, 0])
    
        let bars = []
        let bottom = 450
        
        data.forEach((datum, index) => {
            bars.push(<Bar start={25} key={index} x={x(datum.name)} y={bottom - 6 - (height - y(datum.rating))} width={20} height={height - y(datum.rating)} />)
        })
    
        return (
            <svg width={this.props.width} height={this.props.height}>
                <YAxis y={40} labels={y.ticks().reverse()} start={-20} end={height - 223} />
                
                <g className="chart" transform={`translate(${margin.left},${margin.top})`}>
                { bars }
                <XAxis x={bottom - 120} labels={xlabs} start={0} end={width} />
                </g>
            </svg>
        );
    }

}

export default BarChart; 