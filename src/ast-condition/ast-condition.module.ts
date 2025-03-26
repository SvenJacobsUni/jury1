import { Module } from '@nestjs/common';
import { AstConditionService } from './ast-condition.service';

/**
 * Modul für AST-Bedingungen
 */
@Module({
  providers: [AstConditionService],
  exports: [AstConditionService],
})
export class AstConditionModule {}
