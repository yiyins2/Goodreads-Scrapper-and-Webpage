import './App.css';
// import './Collapsible.scss';

import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table/css/react-bootstrap-table.css';
import paginationFactory from 'react-bootstrap-table2-paginator';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Collapsible from 'react-collapsible';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import BookSearchForm from './components/BookSearchForm'
import AuthorSearchForm from './components/AuthorSearchForm'
import BookAddForm from './components/BookAddForm'
import AuthorAddForm from './components/AuthorAddForm'
import BookEdit from './components/BookEdit'
import AuthorEdit from './components/AuthorEdit'

import axios from 'axios';
import BarChart from "./components/BarChart"

export default () => {

const [books, setBooks] = useState([]);
const [authors, setAuthors] = useState([]);

/**
 * axios delete request for book and return success/error message 
 * @param {*} book_id book id 
 */
function deleteBook(book_id) {
    axios.delete(`http://localhost:5000/book?id=${book_id}`)
        .then(
            (response) => {
                setBooks(books.filter(book => book.book_id !== book_id));
                toast.success("Successfully deleted book!")
            },
            (error) => {console.log(error);}
        );
}

/**
 * axios delete request for author and return success/error message 
 * @param {*} author_id author id 
 */
function deleteAuthor(author_id) {
    axios.delete(`http://localhost:5000/author?id=${author_id}`)
        .then(
            (response) => {
                setBooks(authors.filter(author => author.author_id !== author_id));
                toast.success("Successfully deleted book!")
            },
            (error) => {console.log(error);}
        );
}

/**
 * book edit put request
 * check input and warn invalid input
 * success message for api success
 * warn message for api failure 
 * @param {*} book the book 
 */
function bookEdit(book) {
    delete book["_id"];
    book["rating"] = parseFloat(book["rating"])
    book["rating_count"] = parseInt(book["rating_count"])
    book["review_count"] = parseInt(book["review_count"])
    if (book["rating"] < 0 || book["rating_count"] < 0 || book["review_count"] < 0) {
        toast.warn("Invalid input!");
    } else {
        axios.put(`http://localhost:5000/book?id=${book.book_id}`, book)
        .then(
            (response) => {
                window.location.reload()
                toast.success("Successfully edited author!")
            },
            (error) => {toast.warn(error.response.data);}
        );
    }
}

/**
 * author edit put request
 * check input and warn invalid input
 * success message for api success
 * warn message for api failure 
 * @param {*} author the author 
 */
function authorEdit(author) {
    delete author["_id"];
    author["rating"] = parseFloat(author["rating"])
    author["rating_count"] = parseInt(author["rating_count"])
    author["review_count"] = parseInt(author["review_count"])
    if (author["rating"] < 0 || author["rating_count"] < 0 || author["review_count"] < 0) {
        toast.warn("Invalid input!");
    } else {
        axios.put(`http://localhost:5000/author?id=${author.author_id}`, author)
        .then(
            (response) => {
                window.location.reload()
                toast.success("Successfully edited author!")
            },
            (error) => {toast.warn(error.response.data);}
        );
    }
}


// book columns header set up 
const book_columns = [{
        dataField: 'delete',
        // make delete request on click 
        formatter: (cell, row) => {
            return (
                <div>
                <button type="button" className="btn btn-outline-danger btn-block mb-1" onClick={() => {
                    var result = window.confirm("Want to delete?");
                    if (result) {
                        deleteBook(row.book_id)}
                    }
                }>
                    Delete
                </button>
                <BookEdit bookEdit={bookEdit} currentBook={row}/>
                </div>
            );
        }
    }, {
        dataField: 'book_id',
        text: 'Book ID'
    }, {
        dataField: 'book_url',
        text: 'Title', 
        formatter: (cell, row) => {
            return <a href={cell}>{row.title}</a>; 
        }, 
        headerStyle: (colum, colIndex) => {
            return { width: '200px'};
        }
    }, {
        dataField: 'ISBN',
        text: 'ISBN'
    }, {
        dataField: 'author_url',
        text: 'Author', 
        formatter: (cell, row) => {
            return <a href={cell}>{row.author}</a>; 
        }, 
        headerStyle: (colum, colIndex) => {
            return { width: '100px'};
        }
    }, {
        dataField: 'image_url',
        text: 'Image', 
        formatter: imgFormatter
    }, {
        dataField: 'rating',
        text: 'Rating'
    }, {
        dataField: 'rating_count',
        text: 'Rating Count'
    }, {
        dataField: 'review_count',
        text: 'Review Count'
    }, {
        // expand similar books 
        dataField: 'similar_books',
        text: 'Similar Books', 
        formatter: (cell, row) => {
            if (typeof row.similar_books !== 'undefined') {
                return (
                    <Collapsible trigger="Click to see similar books">
                        {row.similar_books.map((value, index) => {
                            return <li><a href={value}>{row.similar_books_name[index]}</a></li>
                        })}
                    </Collapsible>
                )
            }
        }
    }
];

// author columns header set up 
const author_columns = [{
        dataField: 'delete',
        // make author delete request on click 
        formatter: (cell, row) => {
            return (
                <div>
                <button type="button" className="btn btn-outline-danger btn-block mb-1" onClick={() => {
                    var result = window.confirm("Want to delete?");
                    if (result) {
                        deleteAuthor(row.author_id)}
                    }
                }>Delete
                </button>
                <AuthorEdit authorEdit={authorEdit} currentAuthor={row}/>
                </div>
            );
        }
    }, {
        dataField: 'author_id',
        text: 'Author ID'
    }, {
        dataField: 'author_url',
        text: 'Name', 
        formatter: (cell, row) => {
            return <a href={cell}>{row.name}</a>; 
        }
    }, {
        dataField: 'image_url',
        text: 'Image', 
        formatter: imgFormatter
    }, {
        dataField: 'rating',
        text: 'Rating'
    }, {
        dataField: 'rating_count',
        text: 'Rating Count'
    }, {
        dataField: 'review_count',
        text: 'Review Count'
    }, {
        // expand author's books 
        dataField: 'author_books',
        text: 'Author\'s Books', 
        formatter: (cell, row) => {
            if (typeof row.author_books !== 'undefined') {
                return (
                    <Collapsible trigger="Click to see author's books">
                    {row.author_books.map((value, index) => {
                        return <li><a href={value}>{row.author_books_name[index]}</a></li>
                    })}
                    </Collapsible>
                )
            }
        }, 
        headerStyle: (colum, colIndex) => {
            return { width: '250px'};
        }
    }, {
        // expand similar authors
        dataField: 'similar_authors',
        text: 'Similar Authors', 
        formatter: (cell, row) => {
            if (typeof row.similar_authors !== 'undefined') {
                return (
                    <Collapsible trigger="Click to see similar authors">
                    
                    {row.similar_authors.map((value, index) => {
                        return <li><a href={value}>{row.similar_authors_name[index]}</a></li>
                    })}
                    </Collapsible>
                )
            }
        }, 
        headerStyle: (colum, colIndex) => {
            return { width: '250px'};
        }
    }
];

/**
 * formatter for images 
 * @param {*} cell the cell to edit 
 * @param {*} row the row information 
 */
function imgFormatter(cell, row) {
    return (
        <div className="text-center">
        <img src={cell} className="rounded mh-100" style={{width: "100px"}}></img>
        </div>
    ); 
}

/**
 * book get search request, success/warn message on api success/failure 
 * @param {*} bookField field of books
 * @param {*} bookQuery query 
 */
function setBookSearch(bookField, bookQuery) {
    axios.get(`http://localhost:5000/search?q=book.${bookField}:${bookQuery}`)
        .then(
            (response) => {
                setBooks([...response.data]);
                toast.success("Successfully searched book!");
            },
            (error) => {
                toast.warn(error.response.data); 
            }
        );
}

/**
 * author get search request, success/warn message on api success/failure 
 * @param {*} authorField field of authors 
 * @param {*} authorQuery query 
 */
function setAuthorSearch(authorField, authorQuery) {
    axios.get(`http://localhost:5000/search?q=author.${authorField}:${authorQuery}`)
        .then(
            (response) => {
                setAuthors([...response.data]);
                toast.success("Successfully searched author!");
            },
            (error) => {
                toast.warn(error.response.data); 
            }
        );
}

/**
 * book post add request, success/warn message on api success/failure 
 * @param {*} book the new book 
 */
function bookAdd(book) {
    book["book_id"] = parseInt(book["book_id"])
    book["rating"] = parseFloat(book["rating"])
    book["rating_count"] = parseInt(book["rating_count"])
    book["review_count"] = parseInt(book["review_count"])
    axios.post("http://localhost:5000/book", book) 
        .then(
            (response) => {
                setBooks([...books, book]);
                toast.success("Successfully added book!");
            },
            (error) => {
                toast.warn("Invalid format"); 
            }
        );
}

/**
 * book post add request, success/warn message on api success/failure 
 * @param {*} author the new author 
 */
function authorAdd(author) {
    author["author_id"] = parseInt(author["author_id"])
    author["rating"] = parseFloat(author["rating"])
    author["rating_count"] = parseInt(author["rating_count"])
    author["review_count"] = parseInt(author["review_count"])
    console.log(author)
    axios.post("http://localhost:5000/author", author) 
        .then(
            (response) => {
                setAuthors([...authors, author]);
                toast.success("Successfully added author!");
            },
            (error) => {
                toast.warn("Invalid format"); 
            }
        );
}

/**
 * initialization for the tables, 
 * set all books and all authors in the database 
 */
useEffect(() => {
    axios.get('http://localhost:5000/search?q=book.book_id:> 0')
        .then(
            (response) => {
                setBooks([...books, ...response.data]);
                setTopKBook(books);
            },
            (error) => {console.log(error);}
        );
    axios.get('http://localhost:5000/search?q=author.author_id:> 0')
        .then(
            (response) => {
                setAuthors([...authors, ...response.data]);
                setTopKAuthor(authors); 
            },
            (error) => {console.log(error);}
        );
}, []);

const [topKBook, setTopKBook] = useState(books); 
const [topKAuthor, setTopKAuthor] = useState(authors); 

/**
 * putting it all together, 
 * also set route for table, and two visualizations
 */
return (
    <div className="container">
    <Router>
    <div>
    <nav>
    <ul>
        <li>
        <Link to="/api">Table</Link>
        </li>
        <li>
        <Link to="/vis/authors">Authors Visualization</Link>
        </li>
        <li>
        <Link to="/vis/books">Books Visualization</Link>
        </li>
    </ul>
    </nav>
    <Switch>
    <Route path="/api">
        <p className="h1">Books</p>
        <div className="row">
        <BookSearchForm setBookSearch={setBookSearch}/>
        <BookAddForm bookAdd={bookAdd}/>
        </div>
        <BootstrapTable 
            keyField='book_id' 
            data={ books } 
            columns={ book_columns } 
            striped
            tabIndexCell
            wrapperClasses="table-responsive"
            pagination={ paginationFactory() }
        />
        <hr className="rounded"></hr>
        <p className="h1">Authors</p>
        <div className="row">
        <AuthorSearchForm setAuthorSearch={setAuthorSearch}/>
        <AuthorAddForm authorAdd={authorAdd}/>
        </div>
        <BootstrapTable 
            keyField='author_id' 
            data={ authors } 
            columns={ author_columns } 
            striped
            tabIndexCell
            wrapperClasses="table-responsive"
            pagination={ paginationFactory() }
        />
        <ToastContainer />
    </Route>
    <Route path="/vis/authors">
        <div class="col-md-6 mb-3">
            <label for="topKAuthor">Input the number of authors to show.</label>
            <input type="text" className="form-control" id="topKAuthor" defaultValue={authors.length}
                onChange={e => setTopKAuthor(authors.sort((a, b) => b.rating - a.rating).slice(0, parseInt(e.target.value)))}></input>
        </div>
        <BarChart width={800} height={500} data={topKAuthor} bookOrAuthor={false}/>
    </Route>
    <Route path="/vis/books">
        <div class="col-md-6 mb-3">
            <label for="topKBook">Input the number of books to show.</label>
            <input type="text" className="form-control" id="topKBook" defaultValue={books.length}
                onChange={e => setTopKBook(books.sort((a, b) => b.rating - a.rating).slice(0, parseInt(e.target.value)))}></input>
        </div>
        <BarChart width={800} height={500} data={topKBook} bookOrAuthor={true}/>
    </Route>
    </Switch>
    </div>
    </Router>
    </div>
)
}
