db = db.getSiblingDB('blog_db');

db.createCollection("posts", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         title: "Post Object Validation",
         required: [ "titre", "auteur", "vues" ],
         properties: {
            titre: {
               bsonType: "string",
               description: "'titre' du post"
            },
            auteur: {
               bsonType: "string",
               description: "'auteur' du post"
            },
            vues: {
               bsonType: "int",
               minimum: 0,
               description: "'vues' sur le post"
            }
         }
      }
   }
});

db.posts.insertMany([
    { titre: "L'Italie", auteur: "Sara", vues: NumberInt(10) },
    { titre: "Les chats", auteur: "Juliette", vues: NumberInt(54) },
    { titre: "La Bierre", auteur: "Fabien", vues: NumberInt(120) },
    { titre: "L'enfance", auteur: "Arthur", vues: NumberInt(5) },
    { titre: "Winx Club", auteur: "Enzo", vues: NumberInt(200) }
]);
