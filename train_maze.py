#!/usr/bin/python

import pygame,sys

# Taken from here: 
# http://stackoverflow.com/questions/7249388/python-duck-typing-for-mvc-event-handling-in-pygame
class WeakBoundMethod:
    def __init__(self, meth):
        import weakref
        self._self = weakref.ref(meth.__self__)
        self._func = meth.__func__

    def __call__(self, *args, **kwargs):
        self._func(self._self(), *args, **kwargs)

class EventManager:
    def __init__(self):
        # does this actually do anything?
        self._listeners = { None : [ None ] }

    def add(self, event_class, event_func):
        print "add %s" % event_class.__name__
        key = event_class.__name__

        try:
          self._listeners[key].append(event_func)
        except KeyError:
          self._listeners[key] = [event_func]

        print "add count %s %s %s" % (event_class, event_func, len(self._listeners[key]))

    def remove(self, eventClass, listener):
        key = eventClass.__name__
        self._listeners[key].remove(listener)

    def post(self, event):
        event_class = event.__class__
        key = event_class.__name__
        print "post event %s (keys %s)" % (
            key, len(self._listeners[key]))
        for listener in self._listeners[key]:
            listener(event)

#------------------------------------------------------------------------------
# Events: PyGame
#------------------------------------------------------------------------------
class Event:
  def __init__(self):
    self.name = "Event"

class QuitEvent(Event):
  def __init__(self):
    self.name = "Quit Event"

class TickEvent(Event):
  def __init__(self):
    self.name = "Tick Event"
  

class RunController:
    def __init__(self, event_mgr):
        event_mgr.add(QuitEvent, self.exit)
        self.running = True
        self.event_mgr = event_mgr

    def exit(self, event):
        print "exit called"
        self.running = False

    def run(self):
        print "run called"
        while self.running:
          event = TickEvent()
          self.event_mgr.post(event)
#------------------------------------------------------------------------------
# Keyboard Controller:
#------------------------------------------------------------------------------
class KeyboardController:

  def __init__(self,event_mgr):
    self.name = "Keyboard Controller"
    self.event_mgr = event_mgr
    event_mgr.add(QuitEvent,self.notify)
    event_mgr.add(TickEvent,self.notify)
    self.events = {QuitEvent.__name__: self.quit,\
                   TickEvent.__name__: self.tick }

  def notify(self,event):
    self.events[event.__class__.__name__](event)

  def quit(self,event):
    print "KeyboardController quit called"

  def tick(self,event):
    print "KeyboardController tick called"

#---------------------------------------- --------------------------------------
# Model: Entities in the game
#------------------------------------------------------------------------------
class Entity(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprint.Sprite.__init__(self)

  def update(self):
    raise NotImplementedError

class TrainCar(Entity):
  def __init__(self,x,y):
    Entity.__init__(self)
  
  def update(self):
    pass

  def animate(self):
    pass


class Tile(Entity):
  def __init__(self,x,y):
    Entity.__init__(self)

  def update(self):
    pass

  def animate(self):
    pass

    

#-------------------------------------------------------------------------------
# View: PyGame
#-------------------------------------------------------------------------------
class Tile
class PygameView:
  def __init__(self, evManager):
		self.event_mgr = evManager
		self.event_mgr.add(TickEvent,self.draw)

		pygame.init()
		self.window = pygame.display.set_mode( (424,440) )
		pygame.display.set_caption( 'Example Game' )
		self.background = pygame.Surface( self.window.get_size() )
		self.background.fill( (0,0,0) )
		font = pygame.font.Font(None, 30)
		text = """Press SPACE BAR to start"""
		textImg = font.render( text, 1, (255,0,0))
		self.background.blit( textImg, (0,0) )
		self.window.blit( self.background, (0,0) )
		pygame.display.flip()

		self.backSprites = pygame.sprite.RenderUpdates()
		self.frontSprites = pygame.sprite.RenderUpdates()

  def draw(self, event):
    print "draw called!"

    # Alert the Event Manager that the QUIT event occurred.
    if pygame.event.get(pygame.QUIT):
      event = QuitEvent()
      self.event_mgr.post(event)

        
def main():

  em = EventManager()
  kb = KeyboardController(em)
  run = RunController(em)
  pygame = PygameView(em)
  run.run()

if __name__ == "__main__":
  main()
