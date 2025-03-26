import { AstConditionResultDto } from './ast-condition-result.dto';

/**
 * Data Transfer Object für AST-Analyseergebnisse
 */
export class AstAnalysisResultDto {
  /**
   * Ergebnisse aller Bedingungen
   */
  conditions: AstConditionResultDto[];

  /**
   * Ob alle erforderlichen Bedingungen erfüllt wurden
   */
  passed: boolean;

  /**
   * Prozentsatz der erfüllten Bedingungen
   */
  score: number;

  /**
   * Fehlermeldung, falls vorhanden
   */
  error?: string;
}
