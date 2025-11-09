from django.core.management.base import BaseCommand
from resort.models import AboutPage

class Command(BaseCommand):
    help = 'Populate the About Page with initial content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating About Page...'))

        about_page, created = AboutPage.objects.get_or_create(
            defaults={
                'title': "OUR STORY",
                'subtitle': "Story Behind Banbas | Sustainability | Chitwan National Park",
                'founders_narrative_title': "Bashu Dhungana's Life Work",
                'founders_narrative_content': """<p>Bashu Dhungana, the visionary behind Banbas, is a lifelong environmentalist and a passionate advocate for sustainable living. His journey began in the buffer zone of Chitwan National Park, where he dedicated himself to preserving the region's rich biodiversity. His tireless efforts in community forestry and anti-poaching initiatives earned him the prestigious Abraham Conservation Award.</p><p>Bashu's commitment extends beyond conservation. He has spearheaded numerous projects to uplift local communities, including establishing libraries and improving infrastructure. His work was recognized with the People's Choice Award by the Bill and Melinda Gates Foundation.</p><p>Banbas is the culmination of Bashu's decades of experience. It is his dream project, a testament to his belief that luxury and sustainability can coexist. Every aspect of Banbas reflects his deep respect for nature and his unwavering commitment to the community.</p>""",
                'founders_narrative_image': "https://www.banbasresort.com/static/img/b.jpg",
                'management_partnership_title': "Management Partnership",
                'management_partnership_content': """<p>To ensure that Banbas delivers a world-class hospitality experience while upholding its core values, Bashu has partnered with Siddhartha Hospitality, a leading Nepalese hospitality brand. This collaboration brings together local expertise and international standards, creating a truly unique and unforgettable guest experience.</p>""",
                'management_partnership_image': "https://www.banbasresort.com/static/img/c.jpg",
                'vision_and_design_title': "Vision and Design",
                'vision_and_design_content': """<p>Bashu's vision for Banbas was clear from the start: to create a resort that is in perfect harmony with its natural surroundings. The design emphasizes eco-friendly architecture, using locally sourced materials and traditional building techniques. The resort is designed to have a minimal impact on the local wildlife and is wheelchair accessible, ensuring that everyone can enjoy the beauty of Chitwan.</p>""",
                'vision_and_design_image': "https://www.banbasresort.com/static/img/a.jpg",
                'main_image': "https://www.banbasresort.com/static/img/b.jpg",
                'secondary_image': "https://www.banbasresort.com/static/img/c.jpg",
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully populated the About Page.'))
        else:
            self.stdout.write(self.style.WARNING('About Page already exists. No changes were made.'))
