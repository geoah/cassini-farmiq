from django.contrib.gis.db import models

class Plot(models.Model):
    name = models.CharField(max_length=100)
    location = models.PolygonField()

    def __str__(self):
        return self.name

class Season(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='seasons')
    crop = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.crop} ({self.start_date} - {self.end_date})"

class SeasonalEvent(models.Model):
    SOIL_PREPARATION = 'soil_preparation'
    GERMINATION = 'germination'
    PLANTING = 'planting'
    FERTILIZATION = 'fertilization'
    PEST_DISEASE = 'pest_disease'
    WEEDING = 'weeding'
    PRUNING_TRIMMING = 'pruning_trimming'
    IRRIGATION = 'irrigation'
    SOIL_TEST = 'soil_test'
    HARVEST = 'harvest'

    EVENT_TYPE_CHOICES = [
        (SOIL_PREPARATION, 'Soil Preparation'),
        (GERMINATION, 'Germination'),
        (PLANTING, 'Planting'),
        (FERTILIZATION, 'Fertilization'),
        (PEST_DISEASE, 'Pest/Disease Presence'),
        (WEEDING, 'Weeding'),
        (PRUNING_TRIMMING, 'Pruning/Trimming'),
        (IRRIGATION, 'Irrigation'),
        (SOIL_TEST, 'Soil Test'),
        (HARVEST, 'Harvest'),
    ]

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    
    # Metadata for specific events
    fertilizer_type = models.CharField(max_length=100, blank=True, null=True)
    fertilizer_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pest_type = models.CharField(max_length=100, blank=True, null=True)
    disease_type = models.CharField(max_length=100, blank=True, null=True)
    irrigation_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    soil_ph = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    harvest_yield = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.event_date}: {self.get_event_type_display()}"

    def save(self, *args, **kwargs):
        # Custom save logic can be added here to validate fields based on event_type
        super(SeasonalEvent, self).save(*args, **kwargs)
