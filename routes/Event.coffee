Event = require '../models/Event'

module.exports =

  # Display a list of story
  show_stories: (req, res) ->
    Event.find({}).exec (err, events) ->
      if err then res.send 500
      else
        res.render 'Event/list',
          title: 'Stories'
          events: events
          count: events.length

  # Display an entry page
  add: (req, res) ->
    res.render 'Event/add_iframe',
      vars:
        url: req.query.url
        doi: req.query.doi

  # Handle POST
  add_post: (req, res) ->
    event = new Event req.body
    coords = req.body['coords'].split ','
    event.coords.lat = coords[0]
    event.coords.lng = coords[1]
    event.save (err, event) ->
      if err then res.send 500, err.message
      else
        res.render 'Event/success'
