from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from .models import Episode
# Create your tests here.

class PodcastTests(TestCase):
    def setUp(self):
        self.episode = Episode.objects.create(
            title = 'Test episode',
            description = 'This the best episode as it is the test episode. I am very proud of this episode',
            pub_date = timezone.now(),
            link = 'https://www.sandarbhdarpan.page/',
            img_url = 'https://1.bp.blogspot.com/-QbWXW4vk4VM/YBQ2BkgnmYI/AAAAAAAAAD8/G45pzHbc8Y0IlBZ9lZyhkhLHSyWMxxIMQCLcBGAsYHQ/s1280/IMG-20210129-WA0056.jpg',
            podcast_name = 'The test podcast',
            guid = 'de194720-7b4c-49e2-a05f-432436d3fetr'
            
            
        )
    def test_content(self):
        self.assertEqual(self.episode.description,'This the best episode as it is the test episode. I am very proud of this episode')
        self.assertEqual(self.episode.link,'https://www.sandarbhdarpan.page/')
        self.assertEqual(self.episode.guid,'de194720-7b4c-49e2-a05f-432436d3fetr')
    def test_str(self):
        self.assertEqual(str(self.episode),'The test podcast : Test episode')
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
    
    def test_home_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response,'homepage.html')
        
    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "This the best episode as it is the test episode. I am very proud of this episode")