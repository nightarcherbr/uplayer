import unittest;

import model;

class LayoutTest(unittest.TestCase):
    def test__layout__valid(self):
        sample = {
            "id": "Layout 1",
            "x": "320/640",
            "y": "240/480",
            "width": "1440/1440",
            "height": "900/900",
            "schedule": [
                {'inicio':'00:00:00', 'fim':'23:00:00'}
            ],
            "frames": [{"id": "master", "width": "1440/1440", "height": "900/900", "x": "0/640", "y": "0/480", "zindex": 1, "grid": [ "Random","Random","Random" ] }]
        }
        layout = model.layout.Layout(sample)
        
        self.assertTrue( layout is not None );
        self.assertEqual( layout.x(), 0.5 );
        self.assertEqual( layout.y(), .5 );
        self.assertEqual( layout.width(), 1 );
        self.assertEqual( layout.height(), 1 );
        self.assertTrue( layout.schedule is not None );
        self.assertTrue( layout.frames is not None );

    def test__layout__invalid_id(self):
        sample = {
            "x": "0/480",
            "y": 0,
            "width": "1440/1440",
            "height": "900/900",
        }

        with self.assertRaises( model.LayoutException ):
            layout = model.layout.Layout(sample)

    def test__layout__invalid_dimension(self):
        sample = {
            "id": "Layout 1",
            "x": "x",
            "y": "0/480",
            "width": "1440/1440",
            "height": "900/900",
        }
        with self.assertRaises( model.LayoutException ):
            layout = model.layout.Layout(sample)

    def test__layout__invalid_frame(self):
        sample = {
            "id": "Layout 1",
            "x": "0/640",
            "y": "0/480",
            "width": "1440/1440",
            "height": "900/900",
            "frames": ["aasd"]
        }
        with self.assertRaises( model.LayoutException ):
            layout = model.layout.Layout(sample)

    # def test__layout__invalid_schedule(self):
    #     sample = {
    #         "id": "Layout 1",
    #         "x": "0/640",
    #         "y": "0/480",
    #         "width": "1440/1440",
    #         "height": "900/900",
    #         "schedule": ["aasd"]
    #     }
    #     with self.assertRaises( model.LayoutException ):
    #         layout = model.layout.Layout(sample)