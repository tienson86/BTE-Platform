# Executive Consulting — Generic Composer

## Rule

**Never** load `PART_08_MASTER_CONSULTING_REPORT.md` for production customer output.

## Flow

```
IntegratedInterpretationContext
  → ExecutiveConsultingPlan (implicit section build)
  → Vietnamese Composer
  → ExecutiveConsultingResult
```

## Target Sections

1. Who you are  
2. How your internal system works  
3. What supports you  
4. What limits you  
5. Current strategic direction  
6. Single most important insight  
7. Three priorities  
8. Three things to avoid  
9. Final consulting conclusion  

## Omitted

Life Timeline / Luck chapter claims when generic Luck interpretation is unavailable (`luck_timeline: OMITTED_NO_GENERIC_LUCK_INTERPRETATION` in diagnostics).

## File

`applications/production/interpretation/executive_composer.py`
