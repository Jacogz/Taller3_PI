import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from a folder"
    
    def handle(self, *args, **kwargs):
        images_folder_path = 'media/generated_images'
        default_image_path = 'generated_images/default.JPG'
        
        # Verifica que el directorio existe
        if not os.path.exists(images_folder_path):
            self.stderr.write(f"Folder '{images_folder_path}' not found.")
            return
        
        # Obtener todas las películas
        movies = Movie.objects.all()
        
        # Obtener imagenes en directorio
        directory = os.listdir(images_folder_path)
        self.stdout.write(f"Found {len(directory)} images in '{images_folder_path}'")
        
        updated_count = 0
        
        for movie in movies:
            title = movie.title
            # Buscar imagen en el directorio
            image_filename = f"m_{title}.png"
            
            image_path = os.path.join('generated_images', image_filename)
            
            try:
                self.stdout.write(f"Processing: {title} image_filename: {image_path}")
                if image_filename in directory:
                    movie.image = image_path
                    movie.save()
                    updated_count += 1
                else:
                    movie.image = default_image_path
                    movie.save()
                    updated_count += 1
                
            except Exception as e:
                self.stderr.write(f"Failed to update {title}: {str(e)}")
                
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies from folder."))