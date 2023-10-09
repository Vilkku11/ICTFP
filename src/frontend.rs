use actix_web::{get, Result, web, App, HttpResponse, HttpServer, Responder};

use actix_files as fs;
use fs::NamedFile;
use std::path::PathBuf;

// Frontend page
async fn frontend() -> Result<fs::NamedFile> {
    let path: PathBuf = PathBuf::from("./frontend/dist/index.html");
    Ok(fs::NamedFile::open(path)?)
}

#[actix_web::main]
pub async fn main() -> std::io::Result<()> {
    println!("Serving frontend :)");
    HttpServer::new(|| {

        App::new().service(
            web::scope("")
                        .route("/", web::get().to(frontend))
                        .service(fs::Files::new("/", "./frontend/dist").index_file("index.html"))
        )
    })
    .bind(("127.0.0.1", 5173))?
    .run()
    .await
}