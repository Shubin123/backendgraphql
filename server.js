const express = require('express');
const expressGraphQL = require('express-graphql').graphqlHTTP;
const {
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLString,
} = require('graphql');

const app = express();
const newschema = new GraphQLSchema({
    
    query: new GraphQLObjectType({
        name: 'hello',
        fields: () => ({
            message: {type: GraphQLString, resolve: () => 'Hello World'}
        })
    }),

});


app.use('/graphql', expressGraphQL({
    schema: newschema,
    graphiql: true

}));
app.listen(9876., () => console.log('Server started on port 9876.'));

